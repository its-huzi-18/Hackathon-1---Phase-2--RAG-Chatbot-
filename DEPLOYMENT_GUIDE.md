# Deployment Guide for RAG Chatbot

## Backend Deployment (Railway)

### Prerequisites
- Railway account
- Access to Qdrant vector database
- Cohere API key

### Environment Variables Required
Set these environment variables in your Railway project:

```
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_URL=your_qdrant_url
COHERE_API_KEY=your_cohere_api_key
TARGET_URL=https://your-frontend-url.vercel.app  # The URL of your deployed frontend
PORT=8000
```

### Deployment Steps
1. Connect your GitHub repository to Railway
2. Set the environment variables as listed above
3. Railway will automatically use the `railway.toml` configuration
4. The backend will be deployed and accessible at the Railway URL

### Populate Knowledge Base
After the first deployment, you need to populate the knowledge base:
1. Run the `process_book.py` script once to populate the vector database:
   ```bash
   python process_book.py
   ```

## Frontend Deployment (Vercel)

### Prerequisites
- Vercel account

### Environment Variables Required
Set these environment variables in your Vercel project:

```
RAG_CHATBOT_API_URL=https://your-backend-url.up.railway.app
NEXT_PUBLIC_RAG_CHATBOT_API_URL=https://your-backend-url.up.railway.app
```

### Deployment Steps
1. Connect your GitHub repository to Vercel
2. Select the `my-book` directory as the project root
3. Set the environment variables as listed above
4. Vercel will automatically build and deploy the Docusaurus site

## Configuration Notes

### API Endpoints
- Health check: `GET /health`
- Ask endpoint: `POST /ask` (for frontend chatbot)
- Query endpoint: `POST /query` (for more detailed queries)

### CORS Settings
The backend allows all origins for development. In production, update api.py to restrict origins.

## Troubleshooting

### Common Issues
1. **CORS errors**: Make sure the frontend can access the backend API
2. **Empty responses**: Ensure the knowledge base has been populated
3. **API key errors**: Verify all API keys are correctly set in environment variables

### Testing the Deployment
1. Verify the backend health: `GET /health` should return the collections
2. Test the ask endpoint with a sample question
3. Check that the frontend chatbot can communicate with the backend