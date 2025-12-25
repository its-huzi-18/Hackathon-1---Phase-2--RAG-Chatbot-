# RAG Chatbot Backend Deployment Guide

This guide explains how to deploy your RAG chatbot backend with complete knowledge of your book.

## Prerequisites

1. **API Keys** (already configured in your `.env` file):
   - Cohere API Key
   - Qdrant Cloud URL and API Key

2. **Python Environment**:
   - Python 3.8+
   - pip or uv package manager

## Setup Instructions

### 1. Install Dependencies

```bash
# Using pip
pip install -r requirements.txt

# Or using uv (recommended)
uv pip install -r requirements.txt
```

### 2. Process Your Book Content

Before starting the API, you need to process your book content and store it in the vector database:

```bash
python process_book.py
```

This will:
- Crawl all pages from your book website (defined in `TARGET_URL` in `.env`)
- Extract text content from each page
- Create embeddings using Cohere
- Store everything in Qdrant vector database

### 3. Start the API Server

```bash
python start_api.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check
- `GET /health` - Check if the API is running
- `GET /collections` - List available collections

### Query Endpoint
- `POST /query` - Query the RAG knowledge base

Request body:
```json
{
  "query": "Your question about the book",
  "top_k": 5,
  "collection_name": "book_knowledge_base"
}
```

Response:
```json
{
  "query": "Your question about the book",
  "response": "Generated answer based on book content",
  "sources": [...],
  "total_chunks": 5
}
```

## Deployment Options

### Option 1: Railway (Free Tier)

1. Install Railway CLI or use the web dashboard
2. Connect to your GitHub repository
3. Create a new project
4. Set the following build command:
   ```
   pip install -r requirements.txt
   ```
5. Set the start command:
   ```
   python start_api.py
   ```
6. Add your environment variables in the Railway dashboard

### Option 2: Render (Free Tier)

1. Create a new Web Service on Render
2. Connect to your GitHub repository
3. Set the runtime to Python
4. Set the build command:
   ```
   pip install -r requirements.txt
   ```
5. Set the start command:
   ```
   uvicorn api:app --host 0.0.0.0 --port $PORT
   ```
6. Add your environment variables in Render dashboard

### Option 3: Vercel (Python support)

1. Go to vercel.com and create an account
2. Import your project from GitHub
3. Set the framework preset to "Python"
4. Add your environment variables
5. Deploy!

## Environment Variables

Make sure these are set in your deployment environment:

```env
COHERE_API_KEY=your_cohere_api_key
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key
TARGET_URL=https://your-book-website.vercel.app/
PORT=8000  # Default, but can be changed
```

## Testing the API

After deployment, test your API:

1. Check health: `GET /health`
2. Test a query:
   ```bash
   curl -X POST http://your-deployed-api-url/query \
     -H "Content-Type: application/json" \
     -d '{
       "query": "What is this book about?",
       "top_k": 3
     }'
   ```

## Troubleshooting

1. **API Key Issues**: Ensure your Cohere and Qdrant API keys are valid
2. **Connection Issues**: Check that your QDRANT_URL is accessible
3. **Empty Results**: Run `process_book.py` again to ensure content is indexed
4. **Rate Limits**: Cohere and Qdrant may have usage limits on free tiers

## Updating Book Content

To update the knowledge base with new content:

1. Update your book website
2. Run `python process_book.py` again
3. The new content will be added to the existing collection