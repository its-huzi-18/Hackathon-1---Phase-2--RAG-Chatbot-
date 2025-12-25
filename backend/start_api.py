#!/usr/bin/env python3
"""
Script to start the RAG Chatbot API server
"""

import os
import subprocess
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        sys.exit(1)

def start_api():
    """Start the API server"""
    print("Starting RAG Chatbot API server...")

    # Import and run the API
    try:
        from api import app
        import uvicorn

        # Get port from environment or default to 8000
        port = int(os.getenv("PORT", 8000))
        print(f"API server starting on port {port}")

        uvicorn.run(app, host="0.0.0.0", port=port)
    except ImportError as e:
        print(f"Error importing API: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting API server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Install dependencies if needed
    if len(sys.argv) > 1 and sys.argv[1] == "--install":
        install_dependencies()

    # Start the API
    start_api()