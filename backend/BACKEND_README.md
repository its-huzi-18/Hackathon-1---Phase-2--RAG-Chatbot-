# RAG Chatbot Backend for Your Book

This backend provides a complete RAG (Retrieval-Augmented Generation) system that gives your chatbot complete knowledge about your book content.

## Overview

The system consists of three main components:

1. **Content Processor**: Crawls your book website and stores content in a vector database
2. **Vector Database**: Stores embedded content for fast similarity search
3. **API Server**: Provides endpoints for querying the knowledge base

## How It Works

1. The content processor crawls all pages of your book website
2. Text content is extracted and split into chunks
3. Each chunk is converted to an embedding vector using Cohere
4. Embeddings are stored in Qdrant vector database with metadata
5. When a query is made, it's converted to a vector and searched against the database
6. Most similar chunks are retrieved and used to generate a response

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Process Your Book Content
```bash
python process_book.py
```

### 3. Start the API Server
```bash
python start_api.py
```

### 4. Test the API
```bash
python test_api.py
```

## Scripts Overview

- `process_book.py` - Crawls your book website and populates the vector database
- `api.py` - Main API server with query endpoints
- `start_api.py` - Script to start the API server
- `run_all.py` - Interactive script to run the complete pipeline
- `test_api.py` - Test script to verify the API is working
- `main.py` - Original RAG pipeline script (updated to use correct collection)

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /collections` - List available collections
- `POST /query` - Query the knowledge base

### Query Endpoint Example

```json
{
  "query": "What are the main topics covered in this book?",
  "top_k": 5,
  "collection_name": "book_knowledge_base"
}
```

## Environment Variables

Make sure your `.env` file contains:

```env
COHERE_API_KEY=your_cohere_api_key
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key
TARGET_URL=https://your-book-website.vercel.app/
PORT=8000
```

## Deployment

For deployment instructions, see [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md).

## Free Hosting Options

### Railway
- Free tier available
- Easy GitHub integration
- Environment variable support

### Render
- Free tier available
- Simple deployment process
- Auto-deploys from GitHub

### Vercel
- Great for frontend-backend combinations
- Easy environment variable management

## Troubleshooting

1. **Empty responses**: Make sure you've run `process_book.py` to populate the database
2. **Connection errors**: Verify your Qdrant URL and API key are correct
3. **API key errors**: Check that your Cohere API key is valid and has sufficient credits
4. **Slow responses**: Consider optimizing chunk size in the processing script

## Updating Content

When you update your book:
1. Run `python process_book.py` again
2. New content will be added to the existing collection
3. Existing content remains available

The system is designed to provide your chatbot with complete knowledge of your book content, enabling it to answer questions accurately based on your material.