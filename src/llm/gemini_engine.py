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

    def generate_answer(self, query: str, context: List[str], sources: List[dict] = None) -> str:
        if sources is None:
            sources = []
            
        if not self.model:
            return "Error: LLM not configured."
            
        context_str = "\n".join(f"[{i+1}] {ctx}" for i, ctx in enumerate(context))
        prompt = f"""
        Voce e um analista de seguranca cibernetica.

        CONTEXTO (relatorios do HackerOne):
        {context_str}

        PERGUNTA: {query}

        INSTRUCOES:
        1. Analise os relatorios fornecidos.
        2. Resuma a tecnica de ataque usada.
        3. Forneca recomendacoes de defesa praticas.
        4. Cite os relatorios usando [1], [2], etc. se relevantes.
        5. IMPORTANTE: RESPONDA SEMPRE EM PORTUGUES (PT-BR).

        RESPOSTA:
        """
        try:
            response = self.model.generate_content(prompt)
            llm_response = response.text
            
            # Append source links to prove authenticity
            if sources:
                source_section = "\n\n" + "="*50 + "\nFONTES (Relatorios Reais do HackerOne):\n"
                seen_links = set()
                for i, src in enumerate(sources, 1):
                    link = src.get('link', 'N/A')
                    if link != 'N/A' and link not in seen_links:
                        seen_links.add(link)
                        source_section += f"[{i}] {src.get('title', 'N/A')} ({src.get('severity', 'N/A')})\n    {link}\n"
                source_section += "="*50
                llm_response += source_section
            
            return llm_response
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            return "Error generating answer from LLM."

