# AI Textbook RAG System

This project implements a Retrieval-Augmented Generation (RAG) system for an AI textbook. It allows users to ask questions about the textbook content and receive accurate answers based on the book's content.

## Features

- Web scraping to extract content from the deployed textbook website
- Text chunking and embedding using Cohere's multilingual embedding model
- Vector storage in Qdrant for efficient similarity search
- FastAPI-based REST API for querying the knowledge base
- Cohere-based response generation with context from the textbook

## Architecture

The system consists of:
- **Processing Pipeline**: Scripts to scrape, chunk, and embed textbook content
- **Vector Database**: Qdrant for storing embeddings
- **API Service**: FastAPI endpoints for querying the knowledge base
- **Frontend**: Docusaurus-based textbook website

## Prerequisites

- Python 3.8+
- Cohere API key
- Qdrant Cloud account or local instance
- Access to the deployed textbook website

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. Set up environment variables in `.env`:
   ```env
   COHERE_API_KEY=your_cohere_api_key
   QDRANT_URL=your_qdrant_url
   QDRANT_API_KEY=your_qdrant_api_key
   TARGET_URL=https://your-textbook-website.com
   ```

## Usage

### 1. Process the textbook content

Run the processing script to scrape and embed the textbook content:

```bash
python backend/process_book.py
```

### 2. Start the API server

```bash
uvicorn backend.api:app --reload
```

### 3. Query the knowledge base

Send POST requests to the `/query` endpoint:

```json
{
  "query": "Your question about the textbook",
  "top_k": 5,
  "collection_name": "book_knowledge_base"
}
```

## Docker Deployment

The system can be deployed using Docker:

```bash
docker build -t ai-textbook-rag .
docker run -p 8000:8000 ai-textbook-rag
```

## Environment Variables

- `COHERE_API_KEY`: Your Cohere API key
- `QDRANT_URL`: URL of your Qdrant instance
- `QDRANT_API_KEY`: API key for Qdrant
- `TARGET_URL`: URL of the textbook website to scrape
- `PORT`: Port to run the API on (default: 8000)

## API Endpoints

- `GET /` - Health check
- `GET /health` - Detailed health check
- `POST /query` - Query the knowledge base
- `GET /collections` - List available collections

## Embedding Model

The system uses Cohere's `embed-multilingual-v3.0` model with 512-dimensional embeddings for broader language compatibility.

## Usage

### 1. Set up environment variables

Create a `.env` file in the project root:

```env
COHERE_API_KEY=your_cohere_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
TARGET_URL=https://your-textbook-website.com
```

### 2. Process the textbook content

Run the processing script to scrape and embed the textbook content:

```bash
python backend/process_book.py
```

### 3. Start the API server

```bash
uvicorn backend.api:app --reload
```

### 4. Use the chatbot

The chatbot is integrated into the Docusaurus website. When you run the website, you'll see a floating chatbot button on the bottom right corner that allows you to ask questions about the book content.

Alternatively, you can query the API directly:

```json
{
  "question": "Your question about the textbook"
}
```

Send this to the `/ask` endpoint, or use the more detailed format with the `/query` endpoint:

```json
{
  "query": "Your question about the textbook",
  "top_k": 5,
  "collection_name": "book_knowledge_base"
}
```

## Chatbot Integration

The chatbot is automatically integrated into the Docusaurus website through the plugin in `docusaurus.config.ts`. The chatbot appears as a floating button on all pages and allows users to ask questions about the book content directly from the website.

## API Endpoints

- `GET /` - Health check
- `GET /health` - Detailed health check
- `POST /query` - Query the knowledge base with full parameters
- `POST /ask` - Simplified endpoint for frontend compatibility
- `GET /collections` - List available collections

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Add your license here]