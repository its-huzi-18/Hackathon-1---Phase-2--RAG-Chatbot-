import os
import argparse
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma

# Load environment variables from .env file
load_dotenv()

def load_and_split_pdf(pdf_path):
    """
    Load PDF document and split it into chunks

    Args:
        pdf_path (str): Path to the PDF file

    Returns:
        list: List of document chunks
    """
    print(f"Loading PDF from: {pdf_path}")

    # Load the PDF document
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    print(f"Loaded {len(documents)} pages from PDF")

    # Split the document into smaller chunks for better retrieval
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,      # Each chunk will have max 1000 characters
        chunk_overlap=200,    # Overlap between chunks to maintain context
        length_function=len,
        is_separator_regex=False,
    )

    texts = text_splitter.split_documents(documents)
    print(f"Split into {len(texts)} text chunks")

    return texts

def create_vector_store(texts, persist_directory):
    """
    Create a vector store from the text chunks using embeddings

    Args:
        texts (list): List of document chunks
        persist_directory (str): Directory to save the vector database
    """
    print("Creating embeddings and vector store...")

    # Initialize embeddings model (using a sentence transformer model)
    # This creates numerical representations of text that can be compared
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    # Create Chroma vector database from documents and embeddings
    # This allows us to efficiently search for similar text
    db = Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
        persist_directory=persist_directory
    )

    print(f"Vector store created and saved to: {persist_directory}")
    return db

def main():
    """
    Main function to run the ingestion process
    """
    # Get paths from environment variables
    book_path = os.getenv("BOOK_PATH", "./../data/book.pdf")
    persist_dir = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")

    # Check if the book file exists
    if not os.path.exists(book_path):
        print(f"Error: Book file not found at {book_path}")
        print("Please place your book.pdf file in the data folder.")
        return

    # Load and split the PDF
    texts = load_and_split_pdf(book_path)

    # Create the vector store
    db = create_vector_store(texts, persist_dir)

    print("\nIngestion completed successfully!")
    print(f"Your book has been processed and stored in: {persist_dir}")
    print("You can now run the chatbot to ask questions about the book.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest a PDF book into a vector database")
    parser.add_argument("--book-path", help="Path to the PDF book file")
    parser.add_argument("--persist-dir", help="Directory to store the vector database")

    args = parser.parse_args()

    # Override environment variables if command line arguments are provided
    if args.book_path:
        os.environ["BOOK_PATH"] = args.book_path
    if args.persist_dir:
        os.environ["CHROMA_PERSIST_DIR"] = args.persist_dir

    main()