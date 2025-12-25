---
sidebar_position: 1
---

# RAG Chatbot Integration

Our book website now includes an AI-powered chatbot that can answer questions about the book content using Retrieval-Augmented Generation (RAG). This allows you to ask questions and get answers based directly on the information in the book.

## How It Works

The RAG chatbot uses the following technology stack:

- **Qdrant**: A vector database for efficient similarity search
- **OpenAI API**: For advanced language understanding (if configured)
- **Google Gemini API**: Alternative language model (if configured)
- **Sentence Transformers**: For creating text embeddings
- **LangChain**: For orchestrating the RAG pipeline

## Using the Chatbot

Look for the chatbot icon in the bottom-right corner of any page. Click on it to open the chat interface, then type your question about the book content. The chatbot will search through the book's content and provide an answer based on relevant passages.

## Technical Details

The chatbot works by:

1. Converting your question into a vector embedding
2. Searching the Qdrant vector database for the most relevant book passages
3. Providing these passages as context to an AI language model
4. Generating a response based on the provided context

If the answer to your question is not in the book content, the chatbot will respond with "Is book me ye information nahi hai".

## Configuration

The chatbot is configured through environment variables in your deployment environment:

- `RAG_CHATBOT_API_URL`: The URL of the backend API server
- `OPENAI_API_KEY`: Your OpenAI API key (optional)
- `GOOGLE_API_KEY`: Your Google Gemini API key (optional)
- `QDRANT_URL`: Qdrant database URL (optional, for cloud)
- `QDRANT_API_KEY`: Qdrant API key (optional, for cloud)