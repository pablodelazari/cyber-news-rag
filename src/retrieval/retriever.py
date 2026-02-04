from typing import List, Any
from loguru import logger

class Retriever:
    def __init__(self, vector_store, embedder, llm=None):
        self.vector_store = vector_store
        self.embedder = embedder
        self.llm = llm

    def standard_search(self, query: str, k: int = 3) -> List[Any]:
        """Performs standard cosine similarity search."""
        query_embedding = self.embedder.embed_query(query)
        results = self.vector_store.search(query_embedding, k=k)
        return results

    def hyde_search(self, query: str, k: int = 3) -> List[Any]:
        """
        Hypothetical Document Embeddings Search.
        Generates a fake document answering the query, then searches for similar real docs.
        """
        if not self.llm:
            logger.warning("LLM not available for HyDE. Falling back to standard search.")
            return self.standard_search(query, k)
        
        logger.info("Generating hypothetical document for HyDE...")
        hypothetical_doc = self.llm.generate(
            f"Escreva um trecho técnico de relatório de vulnerabilidade ou exploit que responda: {query}"
        )
        
        # Use the hypothetical doc to search
        return self.standard_search(hypothetical_doc, k)

    def hybrid_search(self, query: str, k: int = 3) -> List[Any]:
        """
        Combines Semantic Search with simple specific Keyword filtering if applicable.
        (Simplified Hybrid for prototype)
        """
        # In a full production Qdrant setup, we would use Sparse Vectors (BM25) + Dense Vectors.
        # Here we perform a standard search but we could re-rank or filter.
        
        # For now, aliasing to Standard Search to ensure functionality 
        # without complex sparse vector setup in this iteration.
        return self.standard_search(query, k)
