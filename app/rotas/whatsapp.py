# app/rotas/whatsapp.py

from flask import Blueprint, request
from app.utilitarios.extrair_nome import extrair_nome
from app.config.identidade_clinica import carregar_identidade_clinica
from app.utilitarios.configuracoes_clinica import carregar_configuracoes_clinica
from app.agentes.agente_virtual import agente_com_memoria

from twilio.rest import Client
import os
import json

whatsapp = Blueprint("whatsapp", __name__)

def identificar_clinica_por_numero(numero_destino):
    numero_destino_limpo = (
        numero_destino.replace("whatsapp:", "")
                      .replace("+", "")
                      .replace("-", "")
                      .replace("(", "")
                      .replace(")", "")
                      .replace(" ", "")
    )

    for nome_arquivo in os.listdir("configs"):
        if nome_arquivo.endswith(".json"):
            caminho = os.path.join("configs", nome_arquivo)
            with open(caminho, "r", encoding="utf-8") as f:
                dados = json.load(f)
                numero_config = dados.get("contato", {}).get("whatsapp", "")
                numero_config_limpo = (
                    numero_config.replace("+", "")
                                 .replace("-", "")
                                 .replace("(", "")
                                 .replace(")", "")
                                 .replace(" ", "")
                )
                if numero_config_limpo and numero_config_limpo in numero_destino_limpo:
                    return dados.get("clinica_id")

    return "bemquerer"

@whatsapp.route("/webhook", methods=["POST"])
def webhook_whatsapp():
    telefone = request.form.get("From")
    mensagem = request.form.get("Body")
    numero_destino = request.form.get("To")

    if not telefone or not mensagem or not numero_destino:
        return "Requisição inválida", 400

    # Identifica a clínica com base no número Twilio
    clinic_id = identificar_clinica_por_numero(numero_destino)

    # ⚙️ Carrega identidade da clínica (não obrigatório ainda, mas já previsto)
    carregar_identidade_clinica(clinic_id)
    nome_detectado = extrair_nome(mensagem)

    # 🤖 Gera a resposta com agente com memória (LangChain)
    resposta = agente_com_memoria.invoke(
        {"mensagem": mensagem},
        config={"configurable": {"session_id": telefone}}
    )
    print(f"[TESTE LOCAL] Resposta gerada: {resposta.content}")

    # Envia a resposta usando Twilio
    try:
        client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
        client.messages.create(
            body=resposta.content,
            from_=numero_destino,
            to=telefone
        )
    except Exception as e:
        print(f"[ERRO] Falha ao enviar mensagem pelo Twilio: {e}")

    return "ok", 200