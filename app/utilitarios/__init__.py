import os
from twilio.rest import Client

def enviar_mensagem(numero: str, texto: str):
    client = Client(
        os.getenv("TWILIO_ACCOUNT_SID"),
        os.getenv("TWILIO_AUTH_TOKEN")
    )
    from_whatsapp = f"whatsapp:{os.getenv('TWILIO_WHATSAPP_NUMBER')}"
    to_whatsapp = numero if numero.startswith("whatsapp:") else f"whatsapp:{numero}"

    print(f"[ENVIO TWILIO] De: {from_whatsapp} Para: {to_whatsapp} Mensagem: {texto}")

    client.messages.create(
        body=texto,
        from_=from_whatsapp,
        to=to_whatsapp
    )
