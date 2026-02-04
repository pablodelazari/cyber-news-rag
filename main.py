import asyncio
import sys
import os
from dotenv import load_dotenv
from loguru import logger
from src.collector.scraper import HackerOneScraper
from src.collector.api_client import HackerOneAPIClient
from src.processing.chunker import chunker
from src.processing.embedder import Embedder
from src.storage.vector_store import VectorDB
from src.retrieval.retriever import Retriever
from src.retrieval.router import QueryRouter
from src.llm.gemini_engine import GeminiEngine
from src.llm.ollama_engine import OllamaEngine
import yaml

# Load environment variables
load_dotenv()

def load_config():
    with open("config/settings.yaml", "r") as f:
        return yaml.safe_load(f)

async def run_pipeline(query: str):
    logger.info("Starting Cyber News RAG Pipeline...")
    config = load_config()

    # --- INITIALIZATION ---
    logger.info("Initializing components...")
    
    # LLM Selection
    provider = config.get("llm", {}).get("provider", "gemini")
    logger.info(f"Using LLM Provider: {provider.upper()}")
    
    if provider == "ollama":
        llm = OllamaEngine(
            model_name=config["llm"]["model_name"], 
            base_url=config["llm"].get("base_url", "http://localhost:11434")
        )
    else:
        llm = GeminiEngine()
    
    # Embedder & Vector DB
    embedder = Embedder() # Loads model
    vector_store = VectorDB() # Connects to Qdrant
    
    # Retriever & Router
    retriever = Retriever(vector_store, embedder, llm)
    router = QueryRouter(llm)
    
    # --- STEP 1: INGESTION ---
    logger.info("Checking for new reports...")
    
    reports = []
    
    # Try API first if configured
    if config.get("collection", {}).get("method") == "api":
        try:
            logger.info("Attempting to fetch real data from HackerOne API...")
            api_client = HackerOneAPIClient()
            reports = api_client.fetch_new_reports(limit=3)
            
            if not reports:
                logger.warning("API returned no reports (or failed). Falling back to Mock Data for stability.")
                raise Exception("API returned empty list")
                
        except Exception as e:
            logger.error(f"API Failure: {e}")
            logger.info("🔄 ACTIVATING FALLBACK: Switching to Mock Scraper to ensure system operational status.")
            scraper = HackerOneScraper(headless=True)
            reports = scraper.fetch_new_reports(limit=3)
            
    else:
        # Default Mock Mode
        scraper = HackerOneScraper(headless=True)
        reports = scraper.fetch_new_reports(limit=3)
    
    if reports:
        logger.info(f"Found {len(reports)} reports. Processing...")
        all_chunks = []
        
        for report in reports:
            # Metadata to dict
            meta = report.metadata.model_dump()
            # Chunking
            chunks = chunker.chunk_recursive(report.page_content, meta)
            all_chunks.extend(chunks)
        
        if all_chunks:
            logger.info(f"Generated {len(all_chunks)} chunks. Generating embeddings...")
            texts = [c.page_content for c in all_chunks]
            embeddings = embedder.embed_documents(texts)
            
            logger.info("Indexing into Vector Store...")
            vector_store.add_documents(all_chunks, embeddings)
            logger.info("Ingestion complete.")
    else:
        logger.info("No reports fetched.")

    # --- STEP 2: QUERY HANDLING ---
    if not query:
        logger.info("No query provided. Exiting.")
        return

    logger.info(f"Analyzing query: '{query}'")
    strategy = router.route(query)
    logger.info(f"Routing Strategy: {strategy.upper()}")

    context = []
    sources = []  # Store source links for citation
    
    if strategy == "knowledge_base":
        logger.info("Retrieving context from Knowledge Base...")
        results = retriever.hyde_search(query, k=5)
        for res in results:
            payload = res.payload
            context.append(payload.get('page_content', ''))
            # Extract source info from nested metadata
            meta = payload.get('metadata', {})
            sources.append({
                'title': meta.get('title', 'Unknown'),
                'link': meta.get('link', 'N/A'),
                'severity': meta.get('severity', 'N/A')
            })
        logger.info(f"Retrieved {len(context)} documents.")
        
    elif strategy == "web_search":
        logger.warning("Web Search requested but not implemented. Falling back to Knowledge Base.")
        results = retriever.standard_search(query, k=5)
        for res in results:
            payload = res.payload
            context.append(payload.get('page_content', ''))
            meta = payload.get('metadata', {})
            sources.append({
                'title': meta.get('title', 'Unknown'),
                'link': meta.get('link', 'N/A'),
                'severity': meta.get('severity', 'N/A')
            })
        
    elif strategy == "direct_answer":
        logger.info("Direct answer mode (no context needed).")
        context = []
        sources = []

    # --- STEP 3: GENERATION ---
    logger.info("Generating answer...")
    answer = llm.generate_answer(query, context, sources)
    
    print("\n" + "="*50)
    print(f"QUERY: {query}")
    print("-" * 50)
    print(answer)
    print("="*50 + "\n")

if __name__ == "__main__":
    # Allow query from command line arg
    user_query = sys.argv[1] if len(sys.argv) > 1 else "Quais técnicas de XSS recentes foram encontradas?"
    
    try:
        asyncio.run(run_pipeline(user_query))
    except KeyboardInterrupt:
        logger.info("Pipeline stopped by user.")
