# app/modelos/contexto.py

from app.modelos.base import banco
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime

class Contexto(banco.Model):
    __tablename__ = "contexto"

    id_contexto = banco.Column(banco.Integer, primary_key=True)  # Atualizado
    telefone_usuario = banco.Column(banco.String(20), nullable=False, unique=True)
    nome = banco.Column(banco.String(120))
    etapa = banco.Column(banco.String(50), default="saudacao")
    tipo_paciente = banco.Column(banco.String(20))
    motivo = banco.Column(banco.Text)
    dados = banco.Column(JSONB, default=dict)
    criado_em = banco.Column(banco.DateTime, default=datetime.utcnow)
    atualizado_em = banco.Column(banco.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Contexto {self.telefone_usuario}>"