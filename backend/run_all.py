#!/usr/bin/env python3
"""
Script to run the complete RAG Chatbot pipeline:
1. Process book content and store in vector database
2. Start the API server
"""

import os
import sys
import subprocess
import threading
import time
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

def process_book_content():
    """Process book content and populate vector database"""
    print("Processing book content and populating vector database...")
    try:
        from process_book import process_book
        process_book()
        print("Book content processing completed!")
    except ImportError as e:
        print(f"Error importing process_book: {e}")
        print("Make sure you have installed the dependencies first.")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing book content: {e}")
        sys.exit(1)

def start_api_server():
    """Start the API server"""
    print("Starting API server...")
    try:
        from api import app
        import uvicorn

        # Get port from environment or default to 8000
        port = int(os.getenv("PORT", 8000))
        print(f"API server starting on port {port}")
        print(f"API server is ready at http://localhost:{port}")
        print("API documentation available at http://localhost:{port}/docs")

        uvicorn.run(app, host="0.0.0.0", port=port)
    except ImportError as e:
        print(f"Error importing API: {e}")
        print("Make sure you have installed the dependencies first.")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting API server: {e}")
        sys.exit(1)

def main():
    """Main function to run the complete pipeline"""
    print("RAG Chatbot Pipeline")
    print("="*50)

    # Check if user wants to install dependencies
    if len(sys.argv) > 1 and sys.argv[1] == "--install":
        install_dependencies()
        return

    # Ask user what they want to do
    print("\nOptions:")
    print("1. Process book content only")
    print("2. Start API server only")
    print("3. Process content then start API server")
    print("4. Install dependencies")
    print("5. Help")

    choice = input("\nEnter your choice (1-5) or press Enter for option 3: ").strip()

    if choice == "1":
        process_book_content()
    elif choice == "2":
        start_api_server()
    elif choice == "3" or choice == "":
        print("\nStep 1: Processing book content...")
        process_book_content()

        print("\nStep 2: Starting API server...")
        start_api_server()
    elif choice == "4":
        install_dependencies()
    elif choice == "5":
        print("\nHELP:")
        print("- Process book content: Crawls your book website and stores content in vector database")
        print("- Start API server: Runs the chatbot API that can answer questions about your book")
        print("- Process then start: First processes content, then starts the API server")
        print("- Install dependencies: Installs all required Python packages")
    else:
        print("Invalid choice. Please run again and select 1-5.")

if __name__ == "__main__":
    main()