from flask import Flask
from config import Configuracoes
from app.modelos.base import banco
from flask_migrate import Migrate
from app.modelos import especialidade

# Importações de rotas
from app.rotas.whatsapp import whatsapp

# Inicializa o Flask-Migrate
migrate = Migrate()

def criar_aplicacao():
    app = Flask(__name__)
    app.config.from_object(Configuracoes)

    banco.init_app(app)
    migrate.init_app(app, banco)   # ✅ Integra o banco ao Migrate

    app.register_blueprint(whatsapp)

    @app.route("/")
    def verificar_status():
        return "✅ Atendente Virtual no ar!"

    return app


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Configuracoes

banco = SQLAlchemy()
migrate = Migrate()

def criar_aplicacao():
    app = Flask(__name__)
    app.config.from_object(Configuracoes)

    banco.init_app(app)
    migrate.init_app(app, banco)

    return app