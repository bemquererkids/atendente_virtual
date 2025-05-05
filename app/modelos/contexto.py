# app/modelos/contexto.py

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.dialects.postgresql import JSONB
from app.modelos.base import banco
from datetime import datetime

class Contexto(banco.Model):
    __tablename__ = "contexto"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    telefone_usuario = Column(String, nullable=False, unique=True)
    ultima_interacao = Column(Text)
    ultima_resposta = Column(Text)
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    etapa = Column(String)
    nome = Column(String)
    dados = Column(JSONB)
    intensidade_dor = Column(String)
    especialidade = Column(String)
    bairro = Column(String)
    cidade = Column(String)
    motivo = Column(Text)
    tipo_paciente = Column(String)