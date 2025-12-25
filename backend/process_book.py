#!/usr/bin/env python3
"""
Script to process the book content and populate the vector database
This script will extract content from your Docusaurus site and create embeddings
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

        # Find all links in navigation, sidebar, and main content
        links = soup.find_all('a', href=True)

        urls = set()  # Use set to avoid duplicates
        base_netloc = urlparse(base_url).netloc

        for link in links:
            href = link['href']
            # Convert relative URLs to absolute
            full_url = urljoin(base_url, href)

            # Only add URLs that belong to the same domain and are internal
            if urlparse(full_url).netloc == base_netloc:
                # Filter out external links, just keep internal ones
                if href.startswith('/') or base_url in full_url:
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

        # Focus on main content areas for Docusaurus sites
        # Look for main content containers first
        content_selectors = [
            'main',  # Main content area
            '.main-wrapper',  # Common Docusaurus wrapper
            '.container',  # Container elements
            '.markdown',  # Markdown content
            'article',  # Article elements
            '.theme-doc-markdown',  # Docusaurus markdown theme
            '.doc-content',  # Documentation content
        ]

        text_content = ""
        for selector in content_selectors:
            elements = soup.select(selector)
            if elements:
                for element in elements:
                    text_content += element.get_text() + "\n\n"
                break  # Use the first matching selector

        # If no specific content found, get all text
        if not text_content.strip():
            text_content = soup.get_text()

        # Clean up text - remove extra whitespace
        lines = (line.strip() for line in text_content.splitlines())
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
    Create or recreate a Qdrant collection for storing embeddings

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
            # Check if the existing collection has the correct vector size
            existing_collection_info = client.get_collection(collection_name)
            if existing_collection_info.config.params.vectors.size != vector_size:
                logger.warning(f"Collection '{collection_name}' has incorrect vector size ({existing_collection_info.config.params.vectors.size}), recreating...")
                # Delete the existing collection and create a new one
                client.delete_collection(collection_name)
                logger.info(f"Deleted collection '{collection_name}' to recreate with correct dimensions")

        # Create new collection if it doesn't exist or was deleted
        if collection_name not in collection_names or existing_collection_info.config.params.vectors.size != vector_size:
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
            )
            logger.info(f"Successfully created collection '{collection_name}' with correct dimensions")

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

def process_book():
    """
    Main function to process the book content and populate the vector database
    """
    logger.info("Starting book processing pipeline")

    # Get the target URL from environment variable
    target_url = os.getenv("TARGET_URL", "https://physical-ai-humanoid-robotics.vercel.app/")

    # Step 1: Get all URLs from the book website
    urls = get_all_urls(target_url)
    logger.info(f"Processing {len(urls)} URLs from the book")

    # Step 2: Define collection name
    collection_name = "book_knowledge_base"  # Changed to be more specific

    # Step 3: Create collection
    if not create_collection(collection_name):
        logger.error("Failed to create collection, exiting")
        return

    # Step 4: Process each URL
    processed_count = 0
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
                "processed_at": str(uuid.uuid4())
            }

            save_chunk_to_qdrant(collection_name, chunk, embedding, metadata)

        processed_count += 1
        logger.info(f"Completed processing URL {i+1}/{len(urls)}")

    logger.info(f"Book processing completed! Processed {processed_count}/{len(urls)} URLs successfully.")
    logger.info(f"All content has been stored in the '{collection_name}' collection.")

if __name__ == "__main__":
    process_book()