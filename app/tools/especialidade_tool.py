import json
import os
from typing import Optional, Union
from pydantic import BaseModel
from ast import literal_eval
from langchain.tools import tool

# Caminho padrão do arquivo de especialidades
CAMINHO_JSON = os.path.join("configs", "especialidades_por_clinica.json")

class EntradaEspecialidade(BaseModel):
    clinica_id: str
    especialidade: str

def carregar_dados_especialidade(clinica_id: str, especialidade: str) -> str:
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

    texto = f"🔎 *{especialidade.title()} na nossa clínica*\n\n"
    texto += f"{descricao}\n\n"
    texto += f"O atendimento é realizado pela {profissional}.\n\n"
    if diferenciais:
        texto += "✨ *Nossos diferenciais:*\n"
        for item in diferenciais:
            texto += f"- {item}\n"
    return texto.strip()

@tool
def responder_especialidade(input_data: Union[str, dict]) -> str:
    """Responde com detalhes sobre uma especialidade oferecida por uma clínica específica. Espera um JSON com 'clinica_id' e 'especialidade'."""
    try:
        # Se for string, tenta converter para dict
        if isinstance(input_data, str):
            input_data = literal_eval(input_data)

        entrada = EntradaEspecialidade(**input_data)
        return carregar_dados_especialidade(entrada.clinica_id, entrada.especialidade)
    except Exception as e:
        return (
            "⚠️ Não consegui identificar essa especialidade. "
            "Tente perguntar de outra forma ou verifique os dados fornecidos. "
            f"(Erro interno: {e})"
        )