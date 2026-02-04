from typing import List
from loguru import logger

class RAGEvaluator:
    def __init__(self, llm, retriever):
        self.llm = llm
        self.retriever = retriever

    def generate_questions(self, document_text: str) -> List[str]:
        """Generates test questions based on a document text."""
        if not self.llm: return []
        
        prompt = f"""
        Gere 3 perguntas técnicas específicas que podem ser respondidas APENAS lendo o seguinte relatório de segurança:
        
        {document_text[:2000]}...

        Retorne apenas as perguntas, uma por linha.
        """
        response = self.llm.generate(prompt)
        questions = [q.strip() for q in response.split('\n') if q.strip()]
        return questions

    def evaluate_retrieval(self, question: str, expected_content_snippet: str) -> bool:
        """
        Checks if the expected content is returned in the top-k results.
        """
        results = self.retriever.standard_search(question, k=3)
        retrieved_texts = [res.payload['page_content'] for res in results]
        
        # Simple string matching for evaluation
        for text in retrieved_texts:
            if expected_content_snippet in text:
                return True
        return False
