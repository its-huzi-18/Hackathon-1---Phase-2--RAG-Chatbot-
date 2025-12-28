#!/usr/bin/env python3
"""
Start script for the RAG Chatbot API on Railway
This script checks if the knowledge base is populated before starting the API server.
"""
import os
import uvicorn
import logging
from api import app

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_knowledge_base():
    """Check if the knowledge base is already populated"""
    logger.info("Checking if knowledge base needs to be populated...")

    try:
        # Import Qdrant client and other necessary modules
        from qdrant_client import QdrantClient
        from qdrant_client.http import models
        import os

        # Initialize Qdrant client with environment variables
        qdrant_url = os.getenv("QDRANT_URL")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")

        if not qdrant_url or not qdrant_api_key:
            logger.error("QDRANT_URL or QDRANT_API_KEY not found in environment variables")
            return False

        # Parse the URL to extract host properly
        from urllib.parse import urlparse
        parsed_url = urlparse(qdrant_url)
        host = parsed_url.hostname if parsed_url.hostname else qdrant_url.replace("https://", "").replace(":6333", "").split('/')[0]

        client = QdrantClient(
            host=host,
            api_key=qdrant_api_key,
            port=6333 if parsed_url.port else 6333,
            https=True
        )

        collection_name = "book_knowledge_base"

        # Check if collection exists
        try:
            collection_info = client.get_collection(collection_name)
            logger.info(f"Collection '{collection_name}' exists")

            # Check if collection has points (documents)
            count = client.count(
                collection_name=collection_name
            )
            logger.info(f"Collection '{collection_name}' has {count.count} points")

            if count.count > 0:
                logger.info("Knowledge base already populated, skipping population")
                return True
            else:
                logger.info("Knowledge base is empty, needs to be populated")
                return False
        except Exception as e:
            logger.info(f"Collection '{collection_name}' does not exist, needs to be created and populated: {str(e)}")
            return False

    except Exception as e:
        logger.error(f"Error checking knowledge base: {str(e)}")
        # If we can't check, assume it needs to be populated
        return False

def populate_knowledge_base():
    """Populate the knowledge base if it's empty"""
    logger.info("Populating knowledge base...")

    try:
        # Import the process_book functionality
        from process_book import process_book

        # Run the process_book function to populate the knowledge base
        process_book()
        logger.info("Knowledge base population completed.")
        return True
    except Exception as e:
        logger.error(f"Error populating knowledge base: {str(e)}")
        return False

def main():
    # Check if knowledge base needs to be populated
    is_populated = check_knowledge_base()

    if not is_populated:
        logger.info("Knowledge base is not populated, running population script...")
        success = populate_knowledge_base()
        if not success:
            logger.error("Failed to populate knowledge base, but starting server anyway...")
    else:
        logger.info("Knowledge base is already populated, starting server...")

    # Start the API server
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()