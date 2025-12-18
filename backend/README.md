# RAG Chatbot Backend

This backend component handles fetching content from URLs, generating embeddings using Cohere, and storing them in Qdrant vector database.

## Features

- Fetches all URLs from a deployed website
- Extracts text content from each URL
- Chunks text into manageable pieces
- Generates embeddings using Cohere's API
- Stores embeddings in Qdrant vector database

## Prerequisites

- Python 3.8+
- UV package manager
- API keys for Cohere and Qdrant (stored in `.env` file)

## Installation

1. Install UV package manager:
```bash
pip install uv
```

2. Install dependencies:
```bash
uv pip install -r requirements.txt
```

Or using pip:
```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
COHERE_API_KEY=your_cohere_api_key
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key
TARGET_URL=https://your-target-website.com
```

## Usage

Run the main script to start the RAG pipeline:

```bash
python main.py
```

## Functions

- `get_all_urls()`: Fetches all URLs from the target website
- `extract_text_from_url()`: Extracts text content from a URL
- `chunk_text()`: Splits text into overlapping chunks
- `embed()`: Generates embeddings for text chunks
- `create_collection()`: Creates a Qdrant collection
- `save_chunk_to_qdrant()`: Saves text chunks and embeddings to Qdrant