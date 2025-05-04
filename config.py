import os
from dotenv import load_dotenv
load_dotenv()

class Configuracoes:
    CHAVE_SECRETA = os.getenv("CHAVE_SECRETA", "segredo-padrao")
    SQLALCHEMY_DATABASE_URI = os.getenv("URL_BANCO_DADOS")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")