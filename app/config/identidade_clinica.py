import os
import json

def carregar_identidade_clinica(clinic_id: str) -> dict:
    """
    Carrega a identidade da clínica a partir de um arquivo JSON na pasta configs.
    
    Parâmetros:
    - clinic_id: identificador único da clínica (ex: 'bemquerer')

    Retorna:
    - Um dicionário com a identidade da clínica, ou levanta erro se não encontrado.
    """
    pasta_configs = os.path.join(os.path.dirname(__file__), "../../configs")
    caminho_json = os.path.join(pasta_configs, f"{clinic_id}.json")

    if not os.path.exists(caminho_json):
        raise FileNotFoundError(f"❌ Arquivo de configuração não encontrado para a clínica: {clinic_id}")

    with open(caminho_json, "r", encoding="utf-8") as f:
        identidade = json.load(f)

    return identidade