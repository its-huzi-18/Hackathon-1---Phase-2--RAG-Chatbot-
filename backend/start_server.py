#!/usr/bin/env python3
"""
Start script for the RAG Chatbot API on Railway
"""
import os
import uvicorn

# Import the app from the backend directory
from api import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)