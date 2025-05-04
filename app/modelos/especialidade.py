# app/modelos/especialidade.py

from app.modelos.base import banco
from datetime import datetime

class Especialidade(banco.Model):
    __tablename__ = "especialidades"

    id = banco.Column(banco.Integer, primary_key=True)
    nome = banco.Column(banco.String(100), nullable=False)
    palavras_chave = banco.Column(banco.Text, nullable=True)  # armazenado como JSON string
    resposta = banco.Column(banco.Text, nullable=True)
    profissional = banco.Column(banco.String(100), nullable=True)
    criado_em = banco.Column(banco.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Especialidade {self.nome}>"