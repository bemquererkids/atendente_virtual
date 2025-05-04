# app/modelos/profissional.py

from app.modelos.base import banco
from sqlalchemy import Column, Integer, String

class Profissional(banco.Model):
    __tablename__ = "profissionais"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    especialidade = Column(String, nullable=False)

    def __repr__(self):
        return f"<Profissional {self.nome} — {self.especialidade}>"