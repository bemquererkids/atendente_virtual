# ✅ Arquivo principal da aplicação Flask

from flask import Flask
from flask_migrate import Migrate

# Importa a base de dados com SQLAlchemy
from app.modelos.base import banco

# Carrega as configurações da aplicação (ex: banco, chave secreta, etc.)
from config import Configuracoes

# Importa o blueprint com a rota do WhatsApp
from app.rotas.whatsapp import whatsapp

# Inicializa o Flask-Migrate para suporte a migrações com Alembic
migrate = Migrate()

# 🔧 Função que cria e configura a aplicação Flask
def criar_aplicacao():
    app = Flask(__name__)

    # Carrega as configurações definidas em config.py
    app.config.from_object(Configuracoes)

    # Inicializa o banco de dados com a app
    banco.init_app(app)

    # Liga o Migrate à app e ao banco
    migrate.init_app(app, banco)

    # Registra o blueprint das rotas do WhatsApp
    app.register_blueprint(whatsapp)

    # Rota de teste para verificar se o servidor está no ar
    @app.route("/")
    def verificar_status():
        return "✅ Atendente Virtual no ar!"

    return app