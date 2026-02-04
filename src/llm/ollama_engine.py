import requests
import json
from loguru import logger
from typing import List

class OllamaEngine:
    def __init__(self, model_name: str = "llama3", base_url: str = "http://localhost:11434"):
        self.model = model_name
        self.base_url = base_url
        self.api_generate = f"{base_url}/api/generate"
        logger.info(f"Initialized OllamaEngine with model: {model_name} at {base_url}")

    def generate(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        try:
            response = requests.post(self.api_generate, json=payload)
            response.raise_for_status()
            return response.json().get("response", "")
        except Exception as e:
            logger.error(f"Ollama generation failed: {e}")
            return "Error: Could not connect to Local AI."

    def generate_answer(self, query: str, context: List[str], sources: List[dict] = None) -> str:
        if sources is None:
            sources = []
            
        context_str = "\n".join(f"[{i+1}] {ctx}" for i, ctx in enumerate(context))
        
        # Red Teamer Persona Prompt
        prompt = f"""
        [SYSTEM]
        Voce e um Red Teamer Senior e Especialista em AppSec.
        Sua tarefa e analisar vulnerabilidades com profundidade tecnica, explicando a 'Root Cause' e verificando deteccao.
        
        [CONTEXTO - RELATORIOS REAIS DO HACKERONE]
        {context_str}

        [PERGUNTA DO USUARIO]
        {query}

        [INSTRUCOES]
        1. Explique tecnica e detalhadamente como a falha ocorre (Root Cause Analysis).
        2. Avalie se o OWASP Top 10 for LLM (Large Language Model Applications) se aplica.
        3. Diga se uma IA (SAST/DAST com IA) poderia ter ajudado e como.
        4. Seja direto, tecnico e use terminologia de seguranca ofensiva.
        5. IMPORTANTE: RESPONDA SEMPRE EM PORTUGUES (PT-BR).
        6. Ao final, SEMPRE cite os relatorios usando [1], [2], etc.
        
        [RESPOSTA]
        """
        
        llm_response = self.generate(prompt)
        
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

