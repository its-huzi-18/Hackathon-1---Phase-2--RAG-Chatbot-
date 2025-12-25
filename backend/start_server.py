#!/usr/bin/env python3
"""
Start script for the RAG Chatbot API on Railway
"""
import os
from api import app
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)