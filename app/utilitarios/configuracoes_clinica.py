import os
import json
import re

def limpar_numero(numero):
    """Remove tudo que não é dígito do telefone."""
    return re.sub(r"\D", "", numero or "")

def mapear_telefone_para_clinica_id(numero: str) -> str:
    """
    Mapeia um número de telefone para o ID da clínica correspondente.
    
    Parâmetro:
    - numero: string com telefone no formato internacional (ex: +5511999998888)
    
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