import os
import google.generativeai as genai
from typing import List
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

class GeminiEngine:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            logger.warning("GOOGLE_API_KEY not found in environment variables. LLM features will fail.")
            self.model = None
        else:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-pro')

    def generate(self, prompt: str) -> str:
        if not self.model:
            return "Error: LLM not configured."
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error generating content: {e}")
            return "Error generating response."

    def generate_answer(self, query: str, context: List[str]) -> str:
        if not self.model:
            return "Error: LLM not configured."
            
        context_str = "\n".join(f"[{i+1}] {ctx}" for i, ctx in enumerate(context))
        prompt = f"""
        Você é um analista de segurança cibernética.

        CONTEXTO (relatórios do HackerOne):
        {context_str}

        PERGUNTA: {query}

        INSTRUÇÕES:
        1. Analise os relatórios fornecidos.
        2. Resuma a técnica de ataque usada.
        3. Forneça recomendações de defesa práticas.
        4. Cite os relatórios usando [1], [2], etc. se relevantes.
        5. Se o contexto for vazio ou irrelevante, responda com seu conhecimento geral mas avise.

        RESPOSTA:
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            return "Error generating answer from LLM."
