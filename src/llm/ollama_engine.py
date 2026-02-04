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

    def generate_answer(self, query: str, context: List[str]) -> str:
        context_str = "\n".join(f"[{i+1}] {ctx}" for i, ctx in enumerate(context))
        
        # Red Teamer Persona Prompt
        prompt = f"""
        [SYSTEM]
        Você é um Red Teamer Sênior e Especialista em AppSec.
        Sua tarefa é analisar vulnerabilidades com profundidade técnica, explicando a 'Root Cause' e verificando detecção.
        
        [CONTEXTO - RELATÓRIOS DO HACKERONE]
        {context_str}

        [PERGUNTA DO USUÁRIO]
        {query}

        [INSTRUÇÕES]
        1. Explique tecnica e detalhadamente como a falha ocorre (Root Cause Analysis).
        2. Avalie se o OWASP Top 10 for LLM (Large Language Model Applications) se aplica.
        3. Diga se uma IA (SAST/DAST com IA) poderia ter ajudado e como.
        4. Seja direto, técnico e use terminologia de segurança ofensiva.
        
        [RESPOSTA]
        """
        
        return self.generate(prompt)
