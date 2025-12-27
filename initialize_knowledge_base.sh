#!/bin/bash
# Script to initialize the knowledge base for the RAG Chatbot
# Run this script after deploying the backend to populate the vector database

echo "Initializing RAG Chatbot knowledge base..."

# Navigate to the backend directory
cd backend

# Run the process_book.py script to populate the knowledge base
python process_book.py

echo "Knowledge base initialization completed!"