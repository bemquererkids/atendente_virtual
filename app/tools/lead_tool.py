from langchain.tools import tool
from app.modelos.base import banco

@tool
def registrar_lead(nome: str, telefone: str, observacoes: str = "") -> str:
    """Registra um novo lead no banco de dados."""
    novo_lead = Lead(nome=nome, telefone=telefone, observacoes=observacoes)
    banco.session.add(novo_lead)
    banco.session.commit()
    return f"Lead {nome} registrado com sucesso!"
