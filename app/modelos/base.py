from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

banco = SQLAlchemy()

# Histórico de Conversas
class HistoricoConversa(banco.Model):
    __tablename__ = "historico_conversas"

    id = banco.Column(banco.Integer, primary_key=True)
    telefone_usuario = banco.Column(banco.String)
    mensagem = banco.Column(banco.Text)
    resposta = banco.Column(banco.Text)
    data_hora = banco.Column(banco.DateTime, default=datetime.utcnow)



class Clinica(banco.Model):
    __tablename__ = "clinicas"

    id = banco.Column(banco.Integer, primary_key=True)
    nome = banco.Column(banco.String)
    cidade = banco.Column(banco.String)
    nome_secretaria = banco.Column(banco.String)
    contexto_comunicacao = banco.Column(banco.Text)

# Contexto da Conversa
class Contexto(banco.Model):
    __tablename__ = "contexto"

    id = banco.Column(banco.Integer, primary_key=True)
    telefone_usuario = banco.Column(banco.String)
    ultima_interacao = banco.Column(banco.Text, nullable=True)
    ultima_resposta = banco.Column(banco.Text, nullable=True)
    criado_em = banco.Column(banco.DateTime, default=datetime.utcnow)
    atualizado_em = banco.Column(banco.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    etapa = banco.Column(banco.String)
    nome = banco.Column(banco.String)
    dados = banco.Column(banco.JSON)
    intensidade_dor = banco.Column(banco.String)
    especialidade = banco.Column(banco.String)
    bairro = banco.Column(banco.String)
    cidade = banco.Column(banco.String)
    motivo = banco.Column(banco.String)
    tipo_paciente = banco.Column(banco.String)


# Perguntas Frequentes
class PerguntaFrequente(banco.Model):
    __tablename__ = "perguntas_frequentes"

    id = banco.Column(banco.Integer, primary_key=True)
    clinica_id = banco.Column(banco.Integer, banco.ForeignKey("clinicas.id"))
    pergunta = banco.Column(banco.Text)
    resposta = banco.Column(banco.Text)



# Leads (Pacientes Interessados)
class Lead(banco.Model):
    __tablename__ = "leads"

    id = banco.Column(banco.Integer, primary_key=True)
    clinica_id = banco.Column(banco.Integer, banco.ForeignKey("clinicas.id"))
    nome = banco.Column(banco.String)
    telefone = banco.Column(banco.String)
    email = banco.Column(banco.String)
    data_nascimento = banco.Column(banco.Date)
    necessidades_especiais = banco.Column(banco.Boolean)
    sindrome = banco.Column(banco.String)
    sedacao = banco.Column(banco.Boolean)
    alergias = banco.Column(banco.Text)
    medicacoes = banco.Column(banco.Text)
    observacoes = banco.Column(banco.Text)
    mensagem = banco.Column(banco.Text)
    resposta = banco.Column(banco.Text)
    criado_em = banco.Column(banco.DateTime, default=datetime.utcnow)
    ultimo_contato = banco.Column(banco.DateTime)
    origem = banco.Column(banco.String)


# Profissionais da Clínica
class Profissional(banco.Model):
    __tablename__ = "profissionais"

    id = banco.Column(banco.Integer, primary_key=True)
    nome = banco.Column(banco.String)
    especialidade = banco.Column(banco.String)

# Configurações de IA por Clínica
class ClinicConfig(banco.Model):
    __tablename__ = "clinic_config"

    id = banco.Column(banco.Integer, primary_key=True, autoincrement=True)
    clinica_id = banco.Column(banco.Integer, banco.ForeignKey("clinicas.id"), nullable=False, unique=True)
    nome_clinica = banco.Column(banco.String, nullable=False)
    config_json = banco.Column(banco.JSON, nullable=False)
    atualizado_em = banco.Column(banco.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
