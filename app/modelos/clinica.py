# app/modelos/clinica.py

from sqlalchemy import Column, Integer, String
from app.modelos.base import banco

class Clinica(banco.Model):
    __tablename__ = "clinicas"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"<Clinica {self.slug}>"
