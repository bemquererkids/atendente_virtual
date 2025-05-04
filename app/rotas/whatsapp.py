from flask import Blueprint, request
from app.utilitarios.conversacao_gpt import responder_paciente
import os
from twilio.rest import Client

whatsapp = Blueprint("whatsapp", __name__)

@whatsapp.route("/webhook", methods=["POST"])
def webhook_whatsapp():
    telefone = request.form.get("From")
    mensagem = request.form.get("Body")

    if not telefone or not mensagem:
        return "Requisição inválida", 400

    resposta = responder_paciente(telefone, mensagem)

    try:
        client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
        from_whatsapp = f"whatsapp:{os.getenv('TWILIO_WHATSAPP_NUMBER')}"
        to_whatsapp = telefone
        client.messages.create(
            body=resposta,
            from_=from_whatsapp,
            to=to_whatsapp
        )
    except Exception as e:
        print(f"[ERRO] Falha ao enviar mensagem pelo Twilio: {e}")

    return "ok", 200
