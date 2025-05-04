# app/modelos/faq.py

from sqlalchemy import Column, Integer, String, Text
from app.modelos.base import banco

class PerguntaFrequente(banco.Model):
    __tablename__ = "perguntas_frequentes"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    clinica_id = Column(String, nullable=False)  # Ex: "bemquerer"
    pergunta = Column(String(255), nullable=False)
    resposta = Column(Text, nullable=False)

    def __repr__(self):
        return f"<FAQ {self.id} - {self.pergunta[:30]}...>"
