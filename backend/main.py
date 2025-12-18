#!/usr/bin/env python3
"""
RAG Chatbot Backend Implementation
This script handles fetching content from URLs, embedding it, and storing in Qdrant vector database.
"""

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import cohere
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
import uuid
from typing import List, Dict, Any
import logging

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

client = QdrantClient(
    url=qdrant_url.replace("https://", "").replace(":6333", ""),
    api_key=qdrant_api_key,
    port=6333,
    https=True
)

def get_all_urls(base_url: str) -> List[str]:
    """
    Fetch all URLs from the deployed website

    Args:
        base_url (str): The base URL of the deployed website

    Returns:
        List[str]: List of all URLs found on the website
    """
    logger.info(f"Fetching URLs from {base_url}")

    try:
        response = requests.get(base_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a', href=True)

        urls = set()  # Use set to avoid duplicates
        for link in links:
            href = link['href']
            full_url = urljoin(base_url, href)

            # Only add URLs that belong to the same domain
            if urlparse(full_url).netloc == urlparse(base_url).netloc:
                urls.add(full_url)

        # Add the base URL itself
        urls.add(base_url)

        logger.info(f"Found {len(urls)} unique URLs")
        return list(urls)

    except Exception as e:
        logger.error(f"Error fetching URLs: {str(e)}")
        return [base_url]  # Return base URL as fallback

def extract_text_from_url(url: str) -> str:
    """
    Extract text content from a given URL

    Args:
        url (str): URL to extract text from

    Returns:
        str: Extracted text content
    """
    logger.info(f"Extracting text from {url}")

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Get text content
        text = soup.get_text()

        # Clean up text - remove extra whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)

        logger.info(f"Extracted {len(text)} characters from {url}")
        return text

    except Exception as e:
        logger.error(f"Error extracting text from {url}: {str(e)}")
        return ""

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
    """
    Split text into overlapping chunks

    Args:
        text (str): Text to chunk
        chunk_size (int): Size of each chunk
        overlap (int): Overlap between chunks

    Returns:
        List[str]: List of text chunks
    """
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)

        # Move start forward by chunk_size minus overlap
        start = end - overlap

        # Handle edge case where remaining text is shorter than chunk_size
        if end >= len(text):
            break

    logger.info(f"Text chunked into {len(chunks)} parts")
    return chunks

def embed(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for a list of texts using Cohere

    Args:
        texts (List[str]): List of texts to embed

    Returns:
        List[List[float]]: List of embeddings
    """
    logger.info(f"Generating embeddings for {len(texts)} texts")

    try:
        response = co.embed(
            texts=texts,
            model="embed-multilingual-v3.0",  # Using multilingual model for broader compatibility
            input_type="search_document"
        )

        embeddings = response.embeddings
        logger.info(f"Generated {len(embeddings)} embeddings")
        return embeddings

    except Exception as e:
        logger.error(f"Error generating embeddings: {str(e)}")
        return []

def create_collection(collection_name: str, vector_size: int = 1024) -> bool:
    """
    Create a Qdrant collection for storing embeddings

    Args:
        collection_name (str): Name of the collection to create
        vector_size (int): Size of the vectors (should match embedding dimension)

    Returns:
        bool: True if collection was created or already exists
    """
    logger.info(f"Creating collection '{collection_name}' with vector size {vector_size}")

    try:
        # Check if collection already exists
        collections = client.get_collections().collections
        collection_names = [col.name for col in collections]

        if collection_name in collection_names:
            logger.info(f"Collection '{collection_name}' already exists")
            return True

        # Create new collection
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
        )

        logger.info(f"Successfully created collection '{collection_name}'")
        return True

    except Exception as e:
        logger.error(f"Error creating collection: {str(e)}")
        return False

def save_chunk_to_qdrant(collection_name: str, text_chunk: str, embedding: List[float], metadata: Dict[str, Any] = None):
    """
    Save a text chunk and its embedding to Qdrant

    Args:
        collection_name (str): Name of the collection to save to
        text_chunk (str): Text chunk to save
        embedding (List[float]): Embedding vector
        metadata (Dict[str, Any]): Additional metadata to store
    """
    logger.info(f"Saving chunk to Qdrant collection '{collection_name}'")

    if metadata is None:
        metadata = {}

    try:
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={
                "text": text_chunk,
                "metadata": metadata
            }
        )

        client.upsert(
            collection_name=collection_name,
            points=[point]
        )

        logger.info("Successfully saved chunk to Qdrant")

    except Exception as e:
        logger.error(f"Error saving chunk to Qdrant: {str(e)}")

def main():
    """
    Main function to execute the RAG pipeline
    """
    logger.info("Starting RAG pipeline execution")

    # Get the target URL from environment variable
    target_url = os.getenv("TARGET_URL", "https://hakhton-ai-textbook.vercel.app/")

    # Step 1: Get all URLs
    urls = get_all_urls(target_url)
    logger.info(f"Processing {len(urls)} URLs")

    # Step 2: Define collection name
    collection_name = "rag_embeddings"

    # Step 3: Create collection
    if not create_collection(collection_name):
        logger.error("Failed to create collection, exiting")
        return

    # Step 4: Process each URL
    for i, url in enumerate(urls):
        logger.info(f"Processing URL {i+1}/{len(urls)}: {url}")

        # Extract text from URL
        text_content = extract_text_from_url(url)

        if not text_content.strip():
            logger.warning(f"No text content found for URL: {url}")
            continue

        # Chunk the text
        text_chunks = chunk_text(text_content)

        # Generate embeddings for chunks
        embeddings = embed(text_chunks)

        if len(embeddings) != len(text_chunks):
            logger.error(f"Mismatch between chunks ({len(text_chunks)}) and embeddings ({len(embeddings)})")
            continue

        # Save each chunk and its embedding to Qdrant
        for j, (chunk, embedding) in enumerate(zip(text_chunks, embeddings)):
            metadata = {
                "source_url": url,
                "chunk_index": j,
                "total_chunks": len(text_chunks),
                "created_at": str(uuid.uuid4())
            }

            save_chunk_to_qdrant(collection_name, chunk, embedding, metadata)

    logger.info("RAG pipeline completed successfully!")

if __name__ == "__main__":
    main()