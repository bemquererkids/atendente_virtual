# app/tools/profissionais_tool.py

from langchain.tools import tool
from app.modelos.profissional import Profissional

@tool
def consultar_profissionais(tool_input: str = "") -> str:
    """
    Retorna lista de profissionais com fallback caso não haja cadastro.
    """
    try:
        profissionais = Profissional.query.all()
        if profissionais:
            return "\n".join([f"{p.nome} — {p.especialidade}" for p in profissionais])
    except:
        pass  # ignora erro se o banco não estiver pronto

    # fallback seguro
    return (
        "Nossa equipe conta com especialistas em ortodontia, odontopediatria, implantes, sedação e estética. "
        "Se quiser, posso sugerir o profissional ideal de acordo com sua necessidade!"
    )
