# app/tools/gpt_tool.py

from langchain.tools import tool
from app.utilitarios.chatgpt import gerar_resposta_informativa

@tool
def responder_gpt_tool(pergunta: str) -> str:
    """
    Ferramenta de fallback para responder perguntas com o modelo padrão da Clara.
    """
    resposta = gerar_resposta_informativa(pergunta)
    if isinstance(resposta, dict) and "content" in resposta:
        return resposta["content"]
    return resposta