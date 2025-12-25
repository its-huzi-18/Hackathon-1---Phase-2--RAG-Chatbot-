import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import HuggingFaceHub  # Using local LLM as alternative to OpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Book RAG Chatbot",
    description="A chatbot that answers questions based only on the content of a specific book",
    version="1.0.0"
)

# Define request/response models
class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str
    source_chunks: List[str] = []

# Global variable to store the vector database
vector_db = None

def initialize_vector_db():
    """
    Initialize the vector database when the application starts
    """
    global vector_db

    persist_directory = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")

    # Check if the vector database exists
    if not os.path.exists(persist_directory):
        raise Exception(f"Vector database not found at {persist_directory}. Please run ingest.py first.")

    # Initialize embeddings model
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    # Load the existing vector database
    vector_db = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )

    print(f"Vector database loaded from: {persist_directory}")

def format_docs(docs):
    """
    Format retrieved documents into a string
    """
    return "\\n\\n".join(doc.page_content for doc in docs)

def create_rag_chain():
    """
    Create the RAG (Retrieval-Augmented Generation) chain
    This connects the document retriever with the LLM
    """
    # Set up the LLM (using a lightweight model that runs locally)
    # Alternative: You can use OpenAI if you have an API key
    import os
    if os.getenv("OPENAI_API_KEY"):
        from langchain_openai import OpenAI
        llm = OpenAI(temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))
    else:
        # Using a lightweight Hugging Face model as fallback
        # Make sure to install huggingface_hub: pip install huggingface_hub
        from langchain_community.llms import HuggingFaceEndpoint
        llm = HuggingFaceEndpoint(
            repo_id="google/flan-t5-small",  # Lightweight model
            temperature=0.1,
            max_new_tokens=512
        )

    # Create the prompt template for the LLM
    # This tells the LLM how to format its response based on retrieved context
    template = """You are a helpful assistant that answers questions based only on the provided context from a book.
    If the answer is not available in the provided context, respond with exactly: "Is book me ye information nahi hai".

    Context: {context}

    Question: {question}

    Answer:"""

    prompt = PromptTemplate.from_template(template)

    # Set up the retriever to get relevant documents from the vector database
    retriever = vector_db.as_retriever(search_kwargs={"k": 3})  # Retrieve top 3 most relevant chunks

    # Create the RAG chain
    # This chain: takes question -> retrieves relevant docs -> formats them -> sends to LLM -> gets answer
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain

@app.on_event("startup")
async def startup_event():
    """
    Event handler that runs when the application starts
    """
    global vector_db
    try:
        initialize_vector_db()

        # Test that we can create the RAG chain
        _ = create_rag_chain()

        print("Application started successfully!")
    except Exception as e:
        print(f"Error during startup: {str(e)}")
        raise

@app.get("/")
async def root():
    """
    Root endpoint to check if the service is running
    """
    return {"message": "Book RAG Chatbot is running!", "status": "ok"}

@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """
    Endpoint to ask a question and get an answer based on the book content

    Args:
        request (QuestionRequest): Request containing the question

    Returns:
        AnswerResponse: Response containing the answer and source chunks
    """
    global vector_db

    if vector_db is None:
        raise HTTPException(status_code=500, detail="Vector database not initialized")

    try:
        # Create the RAG chain
        rag_chain = create_rag_chain()

        # Get the answer from the RAG chain
        answer = rag_chain.invoke(request.question)

        # Also retrieve the source documents to show where the answer came from
        retriever = vector_db.as_retriever(search_kwargs={"k": 3})
        source_docs = retriever.get_relevant_documents(request.question)
        source_chunks = [doc.page_content for doc in source_docs]

        return AnswerResponse(answer=answer, source_chunks=source_chunks)

    except Exception as e:
        print(f"Error processing question: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy", "vector_db_loaded": vector_db is not None}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)