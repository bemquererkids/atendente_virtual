# app/tools/especialidade_tool.py

import json
import os
from langchain_core.tools import tool
from pydantic import BaseModel

# 📍 Caminho para o JSON de especialidades por clínica
CAMINHO_JSON = os.path.join("configs", "especialidades.json")

class EntradaEspecialidade(BaseModel):
    clinica_id: str
    especialidade: str

def carregar_dados_especialidade(clinica_id: str, especialidade: str) -> str:
    """
    Carrega e retorna a resposta personalizada da especialidade de uma clínica.
    """
    if not os.path.exists(CAMINHO_JSON):
        return f"❌ O arquivo de especialidades não foi encontrado em {CAMINHO_JSON}."

    with open(CAMINHO_JSON, "r", encoding="utf-8") as f:
        dados = json.load(f)

    dados_clinica = dados.get(clinica_id, {})
    dados_especialidade = dados_clinica.get(especialidade.lower())

    if not dados_especialidade:
        return f"⚠️ A especialidade '{especialidade}' ainda não está cadastrada para a clínica '{clinica_id}'."

    profissional = dados_especialidade.get("profissional", "um profissional da nossa equipe")
    descricao = dados_especialidade.get("descricao", "")
    diferenciais = dados_especialidade.get("diferenciais", [])

    texto = f"🦷 *{especialidade.title()} na nossa clínica*\n\n"
    texto += f"{descricao}\n\n"
    texto += f"O atendimento é realizado por {profissional}.\n\n"
    if diferenciais:
        texto += "✨ *Nossos diferenciais:*\n"
        for item in diferenciais:
            texto += f"- {item}\n"

    return texto.strip()

@tool(args_schema=EntradaEspecialidade)
def responder_especialidade(clinica_id: str, especialidade: str) -> str:
    """Fornece informações sobre uma especialidade da clínica, com descrição e diferenciais personalizados."""
    return carregar_dados_especialidade(clinica_id, especialidade)