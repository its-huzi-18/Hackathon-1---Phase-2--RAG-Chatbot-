# Quickstart: Embedding Pipeline

## Prerequisites

- Python 3.11+
- UV package manager
- Cohere API key
- Qdrant instance (cloud or local)

## Setup

1. **Initialize the backend project**:
   ```bash
   mkdir backend
   cd backend
   ```

2. **Install UV package manager** (if not already installed):
   ```bash
   pip install uv
   ```

3. **Create requirements.txt**:
   ```txt
   cohere==5.5.8
   qdrant-client==1.9.1
   requests==2.31.0
   beautifulsoup4==4.12.2
   python-dotenv==1.0.0
   ```

4. **Install dependencies**:
   ```bash
   uv pip install -r requirements.txt
   ```

5. **Create environment file**:
   ```bash
   cp .env.example .env
   ```

6. **Add your API keys to .env**:
   ```env
   COHERE_API_KEY=your_cohere_api_key_here
   QDRANT_URL=your_qdrant_url_here
   QDRANT_API_KEY=your_qdrant_api_key_here
   ```

## Usage

1. **Run the embedding pipeline**:
   ```bash
   python main.py
   ```

2. **The pipeline will**:
   - Crawl the Docusaurus site at https://hakhton-1-ai-textbook.vercel.app/
   - Extract text content from all pages
   - Chunk the content into manageable pieces
   - Generate embeddings using Cohere
   - Store the embeddings in Qdrant vector database

## Configuration

- Update the base URL in main.py if needed
- Adjust chunk size and overlap in the chunk_text function
- Modify the Qdrant collection name if needed

## Verification

After running the pipeline:
1. Check logs for successful processing messages
2. Verify embeddings are stored in your Qdrant collection
3. Test similarity search to confirm proper storage