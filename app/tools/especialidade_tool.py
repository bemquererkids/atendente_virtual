import json
import os
from typing import Optional
from pydantic import BaseModel
from langchain.tools import tool

# Caminho atualizado para o novo JSON estruturado por clínica
CAMINHO_JSON = os.path.join("configs", "especialidades_por_clinica.json")

class EntradaEspecialidade(BaseModel):
    clinica_id: str
    especialidade: str

def carregar_dados_especialidade(clinica_id: str, especialidade: str) -> str:
    if not os.path.exists(CAMINHO_JSON):
        return f"❌ O arquivo de especialidades não foi encontrado em {CAMINHO_JSON}."

    with open(CAMINHO_JSON, "r", encoding="utf-8") as f:
        dados = json.load(f)

    dados_clinica = dados.get(clinica_id)
    if not dados_clinica:
        return f"⚠️ A clínica '{clinica_id}' não foi encontrada."

    dados_especialidade = dados_clinica.get(especialidade.lower())
    if not dados_especialidade:
        return f"⚠️ A especialidade '{especialidade}' ainda não está cadastrada para a clínica '{clinica_id}'."

    profissional = dados_especialidade.get("profissional", "um profissional da nossa equipe")
    descricao = dados_especialidade.get("descricao", "")
    diferenciais = dados_especialidade.get("diferenciais", [])

    texto = f"🔎 *{especialidade.title()} na nossa clínica*\n\n"
    texto += f"{descricao}\n\n"
    texto += f"O atendimento é realizado pela {profissional}.\n\n"
    if diferenciais:
        texto += "✨ *Nossos diferenciais:*\n"
        for item in diferenciais:
            texto += f"- {item}\n"
    return texto.strip()

@tool
def responder_especialidade(clinica_id: str, especialidade: str) -> str:
    """Responde com detalhes sobre uma especialidade oferecida por uma clínica específica."""
    try:
        entrada = EntradaEspecialidade(clinica_id=clinica_id, especialidade=especialidade)
        return carregar_dados_especialidade(entrada.clinica_id, entrada.especialidade)
    except Exception:
        return "⚠️ Não consegui identificar essa especialidade. Você poderia reformular ou perguntar de outro jeito?"
