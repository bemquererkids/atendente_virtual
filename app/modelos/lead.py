# app/modelos/lead.py

from sqlalchemy import Column, Integer, String, Date, Boolean, Text, DateTime
from app.modelos.base import banco

class Lead(banco.Model):
    __tablename__ = "leads"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    clinic_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String)
    birth_date = Column(Date)
    special_needs = Column(Boolean, default=False)
    syndrome = Column(String)
    sedation = Column(Boolean, default=False)
    allergies = Column(Text)
    medications = Column(Text)
    notes = Column(Text)
    created_at = Column(DateTime)
    last_contact = Column(DateTime)

    def __repr__(self):
        return f"<Lead {self.name} - {self.phone}>"
