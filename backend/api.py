#!/usr/bin/env python3
"""
RAG Chatbot API Implementation
This script provides API endpoints for querying the RAG knowledge base.
"""

import os
import logging
from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import cohere
from qdrant_client import QdrantClient
from qdrant_client.http.models import SearchRequest
from qdrant_client.http import models
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Cohere client
cohere_api_key = os.getenv("COHERE_API_KEY")
if not cohere_api_key:
    raise ValueError("COHERE_API_KEY not found in environment variables")
co = cohere.Client(cohere_api_key)

# Initialize Qdrant client
qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")
if not qdrant_url or not qdrant_api_key:
    raise ValueError("QDRANT_URL or QDRANT_API_KEY not found in environment variables")

# Parse the URL to extract host properly
from urllib.parse import urlparse
parsed_url = urlparse(qdrant_url)
host = parsed_url.hostname if parsed_url.hostname else qdrant_url.replace("https://", "").replace(":6333", "").split('/')[0]

client = QdrantClient(
    host=host,
    api_key=qdrant_api_key,
    port=6333 if parsed_url.port else 6333,  # Default to 6333 if no port specified
    https=True
)

# Initialize FastAPI app
app = FastAPI(
    title="RAG Chatbot API",
    description="API for querying the RAG knowledge base",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class QueryRequest(BaseModel):
    query: str
    top_k: int = 5
    collection_name: str = "book_knowledge_base"

class QueryResponse(BaseModel):
    query: str
    response: str
    sources: List[Dict[str, Any]]
    total_chunks: int

class HealthResponse(BaseModel):
    status: str
    collections: List[str]

def embed_query(query: str) -> List[float]:
    """
    Generate embedding for a query string using Cohere

    Args:
        query (str): Query text to embed

    Returns:
        List[float]: Embedding vector
    """
    logger.info(f"Generating embedding for query: {query[:50]}...")

    try:
        response = co.embed(
            texts=[query],
            model="embed-multilingual-v3.0",
            input_type="search_query"
        )

        embedding = response.embeddings[0]  # Get the first (and only) embedding
        logger.info(f"Generated embedding with {len(embedding)} dimensions")
        return embedding

    except Exception as e:
        logger.error(f"Error generating query embedding: {str(e)}")
        # Return a default response instead of raising an exception
        logger.warning("Returning default response due to embedding error")
        return [0.0] * 1024  # Return a 1024-dimensional zero vector as fallback

def search_similar_chunks(query_embedding: List[float], collection_name: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Search for similar text chunks in Qdrant

    Args:
        query_embedding (List[float]): Query embedding vector
        collection_name (str): Name of the collection to search in
        top_k (int): Number of results to return

    Returns:
        List[Dict[str, Any]]: List of similar chunks with metadata
    """
    logger.info(f"Searching for similar chunks in collection '{collection_name}', top_k={top_k}")

    # Check what methods are available on the client
    available_methods = [method for method in dir(client) if not method.startswith('_')]
    logger.info(f"Available Qdrant client methods: {[m for m in available_methods if 'search' in m.lower() or 'point' in m.lower()]}")

    # Based on the logs, your Qdrant client has 'query_points' method available
    # This is the correct method to use for your version
    try:
        from qdrant_client.http.models import QueryRequest

        # Use query_points method which is available in your Qdrant client version
        search_result = client.query_points(
            collection_name=collection_name,
            query=query_embedding,
            limit=top_k,
            with_payload=True
        )

        results = []
        for point in search_result.points:
            results.append({
                "text": point.payload.get("text", ""),
                "metadata": point.payload.get("metadata", {}),
                "score": point.score
            })

        logger.info(f"Found {len(results)} similar chunks using query_points method")
        return results

    except AttributeError as e:
        logger.error(f"query_points method not available: {str(e)}")
        # If query_points doesn't work, try the recommend method as a fallback
        try:
            search_result = client.recommend(
                collection_name=collection_name,
                positive=[query_embedding],  # Treat query as positive example
                limit=top_k,
                with_payload=True
            )

            results = []
            for point in search_result:
                results.append({
                    "text": point.payload.get("text", ""),
                    "metadata": point.payload.get("metadata", {}),
                    "score": point.score
                })

            logger.info(f"Found {len(results)} similar chunks using recommend method")
            return results
        except Exception as fallback_error:
            logger.error(f"Fallback search methods also failed: {str(fallback_error)}")
            logger.info(f"Available methods on client: {[m for m in dir(client) if not m.startswith('_') and ('search' in m.lower() or 'point' in m.lower() or 'recommend' in m.lower() or 'query' in m.lower())]}")
            return []
    except Exception as e:
        logger.error(f"Error searching in Qdrant: {str(e)}")
        logger.warning("Returning empty results due to search error")
        return []

def generate_response(query: str, context_chunks: List[Dict[str, Any]]) -> str:
    """
    Generate a response using Cohere Chat API based on the query and context

    Args:
        query (str): User query
        context_chunks (List[Dict[str, Any]]): Context chunks to use for response generation

    Returns:
        str: Generated response
    """
    logger.info(f"Generating response for query: {query[:50]}...")

    # Check if we have any context chunks
    if not context_chunks or len(context_chunks) == 0:
        logger.warning("No context chunks found for the query")
        return "I couldn't find relevant information in the book to answer your question. Please try rephrasing or ask about a different topic from the book."

    # Use the top 3 most relevant chunks for better context while maintaining speed
    top_chunks = context_chunks[:3]
    context = "\n\n".join([chunk["text"] for chunk in top_chunks])

    # Create a balanced message that provides good context
    message = f"""
    You are an AI assistant for the AI Textbook. Your purpose is to answer questions about the book content.
    Answer the user's question based on the context provided below.

    Context information is below:
    ---------------------
    {context}
    ---------------------

    User Query: {query}

    Provide a helpful and accurate answer based on the context. If the context doesn't contain the information needed to answer the question, say so clearly.
    """

    try:
        response = co.chat(
            message=message,
            model="command-r-08-2024",  # Using specific version of command model
            max_tokens=350,  # Increased from 250 to 350 for better answers while still being faster than 500
            temperature=0.25  # Slightly increased from 0.2 for more varied responses
        )

        generated_text = response.text.strip()
        logger.info(f"Generated response with {len(generated_text)} characters")
        return generated_text

    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        # Return a helpful message instead of raising an exception
        return "I encountered an issue generating a response. Please try asking your question again."

@app.get("/")
def root():
    """Root endpoint for health check"""
    return {"message": "RAG Chatbot API is running"}

@app.get("/health", response_model=HealthResponse)
def health_check():
    """Health check endpoint"""
    try:
        collections = client.get_collections().collections
        collection_names = [col.name for col in collections]
        return HealthResponse(status="healthy", collections=collection_names)
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Health check failed")

@app.post("/query", response_model=QueryResponse)
def query_endpoint(request: QueryRequest):
    """
    Query the RAG knowledge base

    Args:
        request (QueryRequest): Query request with query text and parameters

    Returns:
        QueryResponse: Response with answer and sources
    """
    logger.info(f"Received query: {request.query[:50]}...")

    # Generate embedding for the query
    query_embedding = embed_query(request.query)

    # Search for similar chunks in the vector database
    similar_chunks = search_similar_chunks(
        query_embedding,
        request.collection_name,
        request.top_k
    )

    # Generate a response using the context
    response_text = generate_response(request.query, similar_chunks)

    # Prepare the response
    response = QueryResponse(
        query=request.query,
        response=response_text,
        sources=[{
            "text": chunk["text"][:200] + "..." if len(chunk["text"]) > 200 else chunk["text"],  # Truncate for response
            "source_url": chunk["metadata"].get("source_url", ""),
            "score": chunk["score"]
        } for chunk in similar_chunks],
        total_chunks=len(similar_chunks)
    )

    logger.info(f"Query processed successfully, returning {len(similar_chunks)} sources")
    return response


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    question: str
    answer: str


@app.post("/ask", response_model=AskResponse)
def ask_endpoint(request: AskRequest):
    """
    Simplified endpoint for asking questions (for frontend compatibility)

    Args:
        request (AskRequest): Request with a question string

    Returns:
        AskResponse: Response with the answer
    """
    logger.info(f"Received ask request: {request.question[:50]}...")

    # Create a query request with default parameters
    query_request = QueryRequest(
        query=request.question,
        top_k=5,
        collection_name="book_knowledge_base"
    )

    # Process using the existing query endpoint logic
    query_embedding = embed_query(query_request.query)
    similar_chunks = search_similar_chunks(
        query_embedding,
        query_request.collection_name,
        query_request.top_k
    )
    response_text = generate_response(query_request.query, similar_chunks)

    # Prepare the response in the expected format
    response = AskResponse(
        question=request.question,
        answer=response_text
    )

    logger.info("Ask request processed successfully")
    return response

@app.get("/collections")
def get_collections():
    """Get list of available collections"""
    try:
        collections = client.get_collections().collections
        collection_names = [col.name for col in collections]
        return {"collections": collection_names}
    except Exception as e:
        logger.error(f"Error getting collections: {str(e)}")
        raise HTTPException(status_code=500, detail="Error getting collections")

if __name__ == "__main__":
    # Get port from environment or default to 8000
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)