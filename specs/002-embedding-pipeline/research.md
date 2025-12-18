# Research: Embedding Pipeline Implementation

## Decision: Project Structure
**Rationale**: User specifically requested a single file (main.py) system design with backend folder initialization using UV package. This approach maintains simplicity while providing clear separation from the frontend.

**Alternatives considered**:
- Multi-file modular approach (rejected to follow user's single-file requirement)
- Direct integration into existing frontend (rejected for separation of concerns)

## Decision: UV Package Manager
**Rationale**: UV is a fast Python package installer and resolver, written in Rust. It's an excellent choice for managing dependencies efficiently.

**Alternatives considered**:
- pip + requirements.txt (slower, traditional approach)
- Poetry (more complex for simple project)
- Conda (not needed for this use case)

## Decision: Cohere for Embeddings
**Rationale**: Cohere provides high-quality text embeddings with good performance and reliability. It has excellent Python SDK support.

**Alternatives considered**:
- OpenAI embeddings (potentially more expensive)
- Hugging Face transformers (self-hosted, requires more resources)
- Sentence Transformers (local, but less consistent quality)

## Decision: Qdrant for Vector Storage
**Rationale**: Qdrant is a high-performance vector database with good Python client support and efficient similarity search capabilities.

**Alternatives considered**:
- Pinecone (managed, but proprietary)
- Weaviate (good alternative, but Qdrant chosen for familiarity)
- FAISS (Facebook AI Similarity Search, but requires more manual management)

## Decision: Web Scraping Approach
**Rationale**: For Docusaurus sites, we'll use requests + BeautifulSoup4 for reliable HTML parsing and content extraction. Docusaurus sites have predictable structure.

**Alternatives considered**:
- Selenium (more complex, for dynamic content)
- Playwright (overkill for static Docusaurus sites)
- Direct API (not available for deployed static sites)

## Decision: Text Chunking Strategy
**Rationale**: Text will be chunked by semantic boundaries (paragraphs, sections) rather than fixed character counts to maintain context.

**Alternatives considered**:
- Fixed-size chunking (simpler but may break context)
- Sentence-level chunking (may result in too small chunks)

## Decision: URL Crawling Method
**Rationale**: For Docusaurus sites, we'll extract URLs from the sitemap.xml or by parsing navigation links to get all accessible pages.

**Alternatives considered**:
- Recursive crawling (potentially inefficient and may miss pages)
- Manual URL list (not scalable)