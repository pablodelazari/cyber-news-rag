from typing import List, Dict, Any
import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

class VectorDB:
    def __init__(self, path: str = "./qdrant_db", collection_name: str = "hackerone_reports"):
        self.client = QdrantClient(path=path)
        self.collection_name = collection_name
        self.vector_size = 384 # Matches all-MiniLM-L6-v2

        self._ensure_collection()

    def _ensure_collection(self):
        collections = self.client.get_collections()
        exists = any(c.name == self.collection_name for c in collections.collections)
        if not exists:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=self.vector_size, distance=Distance.COSINE)
            )

    def add_documents(self, documents: List[Any], embeddings: List[List[float]]):
        """
        Adds documents to the vector store.
        documents: List of objects with page_content and metadata attributes (e.g., Langchain Documents)
        embeddings: List of vector embeddings corresponding to each document
        """
        points = []
        for i, doc in enumerate(documents):
            # Handle metadata: ensure it's a dict
            payload = {
                "page_content": doc.page_content,
                "metadata": doc.metadata if isinstance(doc.metadata, dict) else doc.metadata.dict()
            }
            
            points.append(PointStruct(
                id=str(uuid.uuid4()),
                vector=embeddings[i],
                payload=payload
            ))
        
        if points:
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )

    def search(self, query_vector: List[float], k: int = 3) -> List[Any]:
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=k
        )
        return results

    def filter(self, metadata_filter: Dict) -> List[Any]:
        # Placeholder for metadata filtering logic
        # Qdrant supports powerful filtering.
        pass
