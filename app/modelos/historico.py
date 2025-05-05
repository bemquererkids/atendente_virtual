# app/modelos/historico.py

from sqlalchemy import Column, Integer, String, Text, DateTime
from app.modelos.base import banco
from datetime import datetime

class HistoricoConversa(banco.Model):
    __tablename__ = "historico_conversa"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    telefone_usuario = Column(String(20), nullable=False)
    mensagem = Column(Text, nullable=False)
    resposta = Column(Text, nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Historico {self.id} - {self.telefone_usuario}>"