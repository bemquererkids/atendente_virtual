# app/testes/verificar_identidade.py

from app.config.identidade_clara import config_clinica, NOME_CLINICA, NOME_SECRETARIA

print("✅ Verificação da Identidade da Clínica:")
print("- Nome da Clínica:", NOME_CLINICA)
print("- Nome da Secretária:", NOME_SECRETARIA)
print("- WhatsApp:", config_clinica.get("contato", {}).get("whatsapp", "⚠️ Não encontrado"))
print("- Especialidades:", config_clinica.get("especialidades_ativas", "⚠️ Não listadas"))