# teste_identidade.py

from app.config.identidade_clinica import carregar_identidade_clinica

dados = carregar_identidade_clinica("bemquerer")
print(dados)