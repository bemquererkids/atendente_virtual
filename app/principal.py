# app/principal.py

from flask import Flask
from flask_migrate import Migrate
from app.modelos.base import banco
from config import Configuracoes

# Importação de rotas
from app.rotas.whatsapp import whatsapp

# Inicializa o Flask-Migrate
migrate = Migrate()

def criar_aplicacao():
    app = Flask(__name__)
    app.config.from_object(Configuracoes)

    banco.init_app(app)
    migrate.init_app(app, banco)

    app.register_blueprint(whatsapp)

    @app.route("/")
    def verificar_status():
        return "✅ Atendente Virtual no ar!"

    return app