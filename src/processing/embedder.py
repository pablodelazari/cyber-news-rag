from typing import List
from sentence_transformers import SentenceTransformer

class Embedder:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        # Load model on init
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, chunks: List[str]) -> List[List[float]]:
        """Gera embeddings para uma lista de chunks de texto"""
        # normalize_embeddings=True improves cosine similarity search
        embeddings = self.model.encode(chunks, normalize_embeddings=True)
        return embeddings.tolist()

    def embed_query(self, query: str) -> List[float]:
        """Gera embedding para uma única consulta"""
        embedding = self.model.encode([query], normalize_embeddings=True)
        return embedding[0].tolist()
