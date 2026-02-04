from loguru import logger

class QueryRouter:
    def __init__(self, llm):
        self.llm = llm

    def route(self, query: str) -> str:
        """
        Decides the strategy: 'knowledge_base', 'web_search', or 'direct_answer'.
        """
        prompt = f"""
        Analise a pergunta e decida a melhor estratégia de recuperação de informação:

        Pergunta: {query}

        Opções:
        - "knowledge_base": se a pergunta é sobre relatórios específicos, detalhes técnicos de vulnerabilidades indexadas, ou busca em base de dados de segurança.
        - "web_search": se a pergunta requer *notícias* muito recentes (ex: desta semana), cotações, ou fatos externos ao conhecimento estático.
        - "direct_answer": se é uma pergunta conceitual simples (ex: O que é XSS?), cumprimentos, ou algo que o LLM sabe responder sem contexto.

        Retorne APENAS uma das strings: knowledge_base, web_search, direct_answer.
        """
        
        try:
            decision = self.llm.generate(prompt).strip().lower()
            logger.info(f"Router Decision: {decision}")
            
            if "knowledge" in decision: return "knowledge_base"
            if "web" in decision: return "web_search"
            if "direct" in decision: return "direct_answer"
            
            return "knowledge_base" # Default safe fallback
            
        except Exception as e:
            logger.error(f"Router failed: {e}")
            return "knowledge_base"
