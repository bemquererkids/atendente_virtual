# ✅ Importações padrão
import json
import os
import re
from typing import Optional, Union
from ast import literal_eval

# ✅ Validação de dados com Pydantic
from pydantic import BaseModel

# ✅ Decorador do LangChain para tornar a função uma Tool oficial
from langchain.tools import tool

# 📍 Caminho padrão para o JSON com todas as especialidades por clínica
CAMINHO_JSON = os.path.join("configs", "especialidades_por_clinica.json")


# 📦 Modelo Pydantic para validar entradas bem formatadas
class EntradaEspecialidade(BaseModel):
    clinica_id: str
    especialidade: str


# 🧠 Função auxiliar que extrai o clinica_id de um texto do tipo: "[clinica_id: bemquerer]"
def extrair_clinica_id(texto: str) -> Optional[str]:
    padrao = r"\[clinica_id:\s*(\w+)\]"
    match = re.search(padrao, texto, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None


# 🧾 Função que carrega os dados da especialidade com base no JSON da clínica
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


# 🔧 Tool oficial LangChain: pode ser chamada diretamente por agentes
@tool
def responder_especialidade(input_data: Union[str, dict]) -> str:
    """
    Responde com detalhes sobre uma especialidade da clínica.
    ➤ Entrada aceita: string com [clinica_id: ...] ou dicionário com 'clinica_id' e 'especialidade'.
    """

    try:
        # 🔍 Caso a entrada seja uma string (texto livre ou JSON textual)
        if isinstance(input_data, str):
            input_data = input_data.strip()

            # ✅ Tenta interpretar como JSON usando literal_eval
            if input_data.startswith("{") and input_data.endswith("}"):
                input_data = literal_eval(input_data)

            # 🧠 Caso seja texto livre com [clinica_id: ...]
            else:
                clinica_id = extrair_clinica_id(input_data)
                if not clinica_id:
                    return "⚠️ Não consegui identificar a clínica. Por favor, inclua algo como [clinica_id: bemquerer]."

                with open(CAMINHO_JSON, "r", encoding="utf-8") as f:
                    dados = json.load(f)

                dados_clinica = dados.get(clinica_id, {})
                texto_normalizado = input_data.lower()

                especialidade = None

                # 🔍 Busca por palavras-chave nas especialidades disponíveis
                for esp, detalhes in dados_clinica.items():
                    for termo in detalhes.get("palavras_chave", []):
                        if termo.lower() in texto_normalizado:
                            especialidade = esp
                            break
                    if especialidade:
                        break

                if not especialidade:
                    return "🤔 Não consegui identificar a especialidade na sua mensagem. Poderia reformular?"

                # Monta o dicionário final para ser validado e usado
                input_data = {"clinica_id": clinica_id, "especialidade": especialidade}

        # ✅ Validação do dicionário final com Pydantic
        entrada = EntradaEspecialidade(**input_data)

        # ✅ Gera resposta final com base na especialidade
        return carregar_dados_especialidade(entrada.clinica_id, entrada.especialidade)

    except Exception as e:
        # 🛑 Mensagem amigável + log do erro técnico para debug
        return (
            "❌ Ocorreu um erro ao tentar responder sobre a especialidade. "
            f"(Detalhes técnicos: {e})"
        )