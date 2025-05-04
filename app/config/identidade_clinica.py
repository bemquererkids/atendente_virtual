# app/config/identidade_clinica.py

import json
import os

CAMINHO_JSON = os.path.join(os.path.dirname(__file__), "../../configs/bemquerer.json")

def carregar_dados_clinica():
    with open(CAMINHO_JSON, "r", encoding="utf-8") as f:
        return json.load(f)

DADOS_CLINICA = carregar_dados_clinica()

# Identidade da secretária virtual (pode ser adaptável)
IDENTIDADE_SECRETARIA = DADOS_CLINICA.get("secretaria_ia", {})
IDENTIDADE_CLINICA = {
    "nome": DADOS_CLINICA.get("nome", "Nossa Clínica"),
    "contato": DADOS_CLINICA.get("contato", {}),
    "responsavel_ti": DADOS_CLINICA.get("responsavel_ti", "")
}