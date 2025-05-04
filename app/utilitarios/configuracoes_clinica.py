import os
import json
import re

def limpar_numero(numero):
    """Remove tudo que não é dígito do telefone (ex: '+55 (11) 91234-5678' → '5511912345678')."""
    return re.sub(r"\D", "", numero or "")

def mapear_telefone_para_clinica_id(numero: str) -> str:
    """
    Mapeia um número de telefone para o ID da clínica correspondente.

    Parâmetro:
    - numero: string com telefone (pode vir com 'whatsapp:', símbolos, etc.)

    Retorna:
    - clinic_id correspondente ou 'bemquerer' como fallback.
    """
    numero_limpo = limpar_numero(numero)

    caminho_json = os.path.join(os.path.dirname(__file__), "../../configs/clinic_id.json")

    if not os.path.exists(caminho_json):
        print("⚠️ Arquivo clinic_id.json não encontrado. Usando fallback padrão.")
        return "bemquerer"

    with open(caminho_json, "r", encoding="utf-8") as f:
        dados = json.load(f)

    for numero_salvo, clinic_id in dados.items():
        if limpar_numero(numero_salvo) == numero_limpo:
            return clinic_id

    return "bemquerer"  # fallback

def carregar_configuracoes_clinica(clinic_id: str) -> dict:
    """
    Carrega o JSON completo de configuração da clínica a partir da pasta configs/.

    Parâmetro:
    - clinic_id: string com o identificador da clínica

    Retorna:
    - Dicionário com as configurações da clínica
    """
    caminho_json = os.path.join(os.path.dirname(__file__), f"../../configs/{clinic_id}.json")

    if not os.path.exists(caminho_json):
        raise FileNotFoundError(f"❌ Configuração não encontrada para a clínica '{clinic_id}'.")

    with open(caminho_json, "r", encoding="utf-8") as f:
        return json.load(f)