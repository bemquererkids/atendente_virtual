# app/modelos/contexto.py

from app.modelos.base import banco
from sqlalchemy import Column, Integer, String, DateTime, Text

class Contexto(banco.Model):
    __tablename__ = "contexto"
    __table_args__ = {'extend_existing': True}

    id_contexto = Column(Integer, primary_key=True)
    telefone_usuario = Column(String)
    ultima_interacao = Column(Text)
    ultima_resposta = Column(Text)
    criado_em = Column(DateTime)
    atualizado_em = Column(DateTime)
    etapa = Column(String)
    nome = Column(String)
    dados = Column(Text)
    intensidade_dor = Column(String)
    especialidade = Column(String)
    bairro = Column(String)
    cidade = Column(String)
    motivo = Column(String)
    tipo_paciente = Column(String)