from typing import List, Any
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings # Updated import for recent langchain
from langchain_experimental.text_splitter import SemanticChunker # Might require langchain-experimental
from langchain.docstore.document import Document
# Note: For 'agentic' and 'semantic', we need specific libraries.
# We will implement the classes as requested.

class ChunkingStrategy:
    def __init__(self):
        # Initialize embeddings for semantic chunking if needed
        # We use a lightweight model for chunking to avoid heavy imports if not used
        self.embedding_model = None 

    def _get_embedding_model(self):
        if not self.embedding_model:
            self.embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        return self.embedding_model

    def chunk_recursive(self, text: str, metadata: dict) -> List[Document]:
        """Implementa RecursiveCharacterTextSplitter"""
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ".", " ", ""]
        )
        chunks = splitter.create_documents([text], metadatas=[metadata])
        return chunks

    def chunk_semantic(self, text: str, metadata: dict) -> List[Document]:
        """Usa sentence-transformers para agrupar content semanticamente"""
        try:
            embeddings = self._get_embedding_model()
            splitter = SemanticChunker(embeddings, breakpoint_threshold_type="percentile")
            chunks = splitter.create_documents([text], metadatas=[metadata])
            return chunks
        except Exception as e:
            print(f"Error in semantic chunking (check dependencies): {e}")
            return self.chunk_recursive(text, metadata)

    def chunk_page(self, text: str, metadata: dict) -> List[Document]:
        """Mantém estrutura original (Whole Document)"""
        # For a web report, 'page' is the whole report usually.
        return [Document(page_content=text, metadata=metadata)]

    def chunk_agentic(self, text: str, metadata: dict) -> List[Document]:
        """LLM decide pontos de divisão"""
        # Placeholder for Agentic Chunking
        # In a real implementation, this would call the LLM to identify logical boundaries.
        # For now, we fall back to recursive or implement a mock.
        return self.chunk_recursive(text, metadata)

chunker = ChunkingStrategy()
