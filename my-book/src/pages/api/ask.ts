import type { NextApiRequest, NextApiResponse } from 'next';
import cohere from 'cohere-ai';
import { QdrantClient } from '@qdrant/js-client-rest';

interface AskRequest {
  question: string;
}

interface AskResponse {
  question: string;
  answer: string;
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<AskResponse | { error: string }>
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { question } = req.body as AskRequest;

    if (!question) {
      return res.status(400).json({ error: 'Question is required' });
    }

    // Initialize Cohere client
    const cohereApiKey = process.env.COHERE_API_KEY;
    if (!cohereApiKey) {
      return res.status(500).json({ error: 'COHERE_API_KEY not found in environment variables' });
    }
    cohere.init(cohereApiKey);

    // Initialize Qdrant client
    const qdrantUrl = process.env.QDRANT_URL;
    const qdrantApiKey = process.env.QDRANT_API_KEY;
    if (!qdrantUrl || !qdrantApiKey) {
      return res.status(500).json({ error: 'QDRANT_URL or QDRANT_API_KEY not found in environment variables' });
    }

    const client = new QdrantClient({
      url: qdrantUrl,
      apiKey: qdrantApiKey,
    });

    // Generate embedding for the query
    const response = await cohere.embed({
      texts: [question],
      model: 'embed-multilingual-v3.0',
      inputType: 'search_query',
    });

    const queryEmbedding = response.body.embeddings[0]; // Get the first (and only) embedding

    // Search for similar chunks in the vector database
    const searchResult = await client.search('book_knowledge_base', {
      vector: queryEmbedding,
      limit: 5,
      with_payload: true,
    });

    const similarChunks = searchResult.map((point: any) => ({
      text: point.payload?.text || '',
      metadata: point.payload?.metadata || {},
      score: point.score,
    }));

    // Check if we have any context chunks
    if (!similarChunks || similarChunks.length === 0) {
      return res.status(200).json({
        question,
        answer: "I couldn't find relevant information in the book to answer your question. Please try rephrasing or ask about a different topic from the book.",
      });
    }

    // Combine context chunks into a single context string
    const context = similarChunks.map(chunk => chunk.text).join('\n\n');

    // Create a message for the chat model
    const message = `
      You are an AI assistant for the AI Textbook. Your purpose is to answer questions about the book content.
      Answer the user's question based on the context provided below.

      Context information is below:
      ---------------------
      ${context}
      ---------------------

      User Query: ${question}

      Provide a helpful and accurate answer based on the context. If the context doesn't contain the information needed to answer the question, say so clearly. Always be helpful and reference the book content when possible.
    `;

    // Generate response using Cohere
    const generateResponse = await cohere.chat({
      message: message,
      model: 'command-r-08-2024',
      max_tokens: 500,
      temperature: 0.3,
    });

    const responseText = generateResponse.body.text?.trim() || '';

    res.status(200).json({
      question,
      answer: responseText,
    });
  } catch (error: any) {
    console.error('Error processing question:', error);
    res.status(500).json({
      error: 'Error processing your question',
    });
  }
}