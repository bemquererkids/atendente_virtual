import json
import os

def carregar_config():
    caminho = os.path.join(os.path.dirname(__file__), "../../configs/bemquerer.json")
    caminho = os.path.abspath(caminho)

    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Arquivo de configuração não encontrado em: {caminho}")

    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)