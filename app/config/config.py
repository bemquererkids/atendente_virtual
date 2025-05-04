import os
import json

def carregar_configuracoes(clinica_id: str = "bemquerer") -> dict:
    """
    Carrega o JSON de configuração da clínica com base no ID.
    """
    caminho = os.path.join(os.path.dirname(__file__), f"../../configs/{clinica_id}.json")
    if not os.path.isfile(caminho):
        raise FileNotFoundError(f"❌ Configuração da clínica não encontrada: {caminho}")

    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)