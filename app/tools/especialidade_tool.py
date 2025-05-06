import json
import os
import re
from typing import Optional
from langchain.tools import tool

CAMINHO_JSON = os.path.join("configs", "especialidades_por_clinica.json")

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

def extrair_clinica_id(texto: str) -> Optional[str]:
    padrao = r"\[clinica_id:\s*(\w+)\]"
    match = re.search(padrao, texto, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None

@tool
def responder_especialidade(input_data: str) -> str:
    """
    Responde com detalhes sobre uma especialidade oferecida por uma clínica.
    A entrada pode ser um JSON ou um texto com '[clinica_id: ...] ...especialidade...'
    """
    try:
        if input_data.strip().startswith("{"):
            # Tenta carregar como JSON
            input_dict = json.loads(input_data)
            clinica_id = input_dict.get("clinica_id")
            especialidade = input_dict.get("especialidade")
        else:
            clinica_id = extrair_clinica_id(input_data)
            if not clinica_id:
                return "⚠️ Não consegui identificar a clínica. Por favor, inclua algo como [clinica_id: bemquerer]."

            with open(CAMINHO_JSON, "r", encoding="utf-8") as f:
                dados = json.load(f)

            dados_clinica = dados.get(clinica_id, {})
            texto_normalizado = input_data.lower()

            especialidade = None
            for esp, detalhes in dados_clinica.items():
                for termo in detalhes.get("palavras_chave", []):
                    if termo.lower() in texto_normalizado:
                        especialidade = esp
                        break
                if especialidade:
                    break

        if not (clinica_id and especialidade):
            return "🤔 Não consegui identificar a especialidade na sua mensagem. Poderia reformular?"

        return carregar_dados_especialidade(clinica_id, especialidade)

    except Exception as e:
        return f"❌ Ocorreu um erro ao tentar responder sobre a especialidade. (Detalhes: {e})"