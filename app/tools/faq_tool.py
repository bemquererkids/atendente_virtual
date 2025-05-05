from langchain.tools import tool
from app.modelos.base import banco
from app.modelos.faq import PerguntaFrequente  # ✅ Correção aqui

# Tool exposta para o agente LangChain — exige {"input": "..."} como argumento
@tool
def buscar_faq(input: str) -> str:
    """
    Usada exclusivamente via LangChain agent. Recebe apenas o campo 'input'.
    """
    return buscar_faq_func(input, clinic_id="bemquerer_odontologia")


# Função real que você pode chamar direto no código Python (como no intencao_router)
def buscar_faq_func(pergunta_usuario: str, clinic_id: str) -> str:
    pergunta = pergunta_usuario.lower().strip()
    if not pergunta or not clinic_id:
        return "Desculpe, preciso de mais informações para te responder com precisão."

    resultados = PerguntaFrequente.query.filter_by(clinica_id=clinic_id).all()

    for item in resultados:
        if item.pergunta.lower() in pergunta or pergunta in item.pergunta.lower():
            return item.resposta

    return "Ainda não tenho essa informação registrada, mas posso confirmar com nossa equipe para você. 💛"