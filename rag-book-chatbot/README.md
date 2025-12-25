# RAG Book Chatbot

This is a Retrieval-Augmented Generation (RAG) chatbot that answers questions based only on the content of a specific book.

## Project Structure

```
rag-book-chatbot/
  backend/
    ingest.py          # Script to process the PDF and create vector database
    chat.py           # FastAPI application for the chatbot
    requirements.txt  # Dependencies
    .env.example      # Example environment variables
  data/
    book.pdf          # Your book file goes here
```

## Setup Instructions

1. **Install dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Set up environment:**
   ```bash
   # Copy the example environment file
   cp .env.example .env

   # Edit .env to add your OpenAI API key if you have one (optional)
   ```

3. **Place your book:**
   - Put your PDF book in the `data/` folder as `book.pdf`
   - Or update the `BOOK_PATH` in `.env` to point to your book

4. **Process your book (create vector database):**
   ```bash
   python ingest.py
   ```
   This will convert your PDF into searchable chunks and store them in a ChromaDB database.

5. **Start the chatbot:**
   ```bash
   python chat.py
   ```
   The chatbot will be available at `http://localhost:8000`

## API Endpoints

- `GET /` - Health check
- `POST /ask` - Ask a question about the book
  - Request body: `{"question": "Your question here"}`
  - Response: `{"answer": "Answer from book", "source_chunks": ["relevant text chunks"]}`

## Example Usage

After starting the server, you can test with curl:

```bash
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"question": "What is RAG?"}'
```

Or use the browser at `http://localhost:8000/docs` to access the interactive API documentation.

## Important Notes

- If the answer is not in the book, the bot will respond with: "Is book me ye information nahi hai"
- Make sure your book is in the data folder before running ingest.py
- The first run will take some time as it processes the PDF and creates embeddings