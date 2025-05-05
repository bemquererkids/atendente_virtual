# popular_especialidades.py

import json
import os
from app.modelos.base import banco
from app.modelos.especialidade import Especialidade
from app.principal import criar_aplicacao
from flask import Flask

CAMINHO_JSON = os.path.join(os.path.dirname(__file__), "configs/bemquerer.json")

def carregar_especialidades_do_json():
    with open(CAMINHO_JSON, "r", encoding="utf-8") as f:
        dados = json.load(f)
        return dados.get("especialidades", {})

def popular_especialidades(app: Flask):
    with app.app_context():
        especialidades = carregar_especialidades_do_json()
        for chave, conteudo in especialidades.items():
            registro = Especialidade(
                nome=chave,
                profissional=conteudo.get("profissional"),
                resposta=conteudo.get("resposta"),
                palavras_chave=",".join(conteudo.get("palavras_chave", []))
            )
            banco.session.add(registro)
        banco.session.commit()
        print("✅ Especialidades populadas com sucesso!")

if __name__ == "__main__":
    app = criar_aplicacao()
    popular_especialidades(app)