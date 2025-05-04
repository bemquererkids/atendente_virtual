# teste_identidade.py

from app.config.identidade_clinica import IDENTIDADE_SECRETARIA, IDENTIDADE_CLINICA

print("🔹 Nome da secretária:", IDENTIDADE_SECRETARIA.get("nome"))
print("🔹 Cargo:", IDENTIDADE_SECRETARIA.get("cargo"))
print("🔹 Apresentação:", IDENTIDADE_SECRETARIA.get("apresentacao"))
print("🔹 Nome da clínica:", IDENTIDADE_CLINICA.get("nome"))
print("🔹 WhatsApp:", IDENTIDADE_CLINICA["contato"].get("whatsapp"))