from langchain.tools import tool
from app.utilitarios.respostas_especialidades import responder_especialidade

@tool
def responder_especialidade_tool(pergunta: str) -> str:
    """
    Tool que interpreta a especialidade solicitada na pergunta do paciente e gera uma resposta personalizada.
    """
    return responder_especialidade(pergunta)