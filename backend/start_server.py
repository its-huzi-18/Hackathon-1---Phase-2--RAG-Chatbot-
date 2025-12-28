#!/usr/bin/env python3
"""
Start script for the RAG Chatbot API on Railway
"""
import os
import uvicorn
import logging
from api import app

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_environment():
    """Check if all required environment variables are set"""
    required_vars = ['QDRANT_API_KEY', 'QDRANT_URL', 'COHERE_API_KEY']
    missing_vars = []

    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        logger.error(f"Missing required environment variables: {missing_vars}")
        return False

    logger.info("All required environment variables are set")
    return True

if __name__ == "__main__":
    # Check environment variables
    if not check_environment():
        logger.error("Environment check failed, exiting...")
        exit(1)

    port = int(os.environ.get("PORT", 8000))
    logger.info(f"Starting server on port {port}")

    # Verify the app is properly loaded
    logger.info(f"API app loaded successfully with {len(app.router.routes)} routes")

    # Print available routes for debugging
    for route in app.router.routes:
        methods = getattr(route, 'methods', 'N/A') if hasattr(route, 'methods') else 'N/A'
        logger.info(f"Available route: {route.path} -> {methods}")

    logger.info("Starting Uvicorn server...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )