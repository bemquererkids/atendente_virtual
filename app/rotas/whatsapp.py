from flask import Blueprint, request
from app.utilitarios.conversacao_gpt import responder_paciente
from app.utilitarios.configuracoes_clinica import carregar_configuracoes_clinica
from twilio.rest import Client
import os
import json

whatsapp = Blueprint("whatsapp", __name__)

def identificar_clinica_por_numero(numero_destino):
    """
    Mapeia o número Twilio de destino (recebedor da mensagem) para um clinic_id baseado nos JSONs da pasta configs/.
    """
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

    return "bemquerer"  # Fallback padrão se nenhuma clínica for identificada

@whatsapp.route("/webhook", methods=["POST"])
def webhook_whatsapp():
    telefone = request.form.get("From")
    mensagem = request.form.get("Body")
    numero_destino = request.form.get("To")

    if not telefone or not mensagem or not numero_destino:
        return "Requisição inválida", 400

    # Identifica a clínica com base no número Twilio de destino
    clinic_id = identificar_clinica_por_numero(numero_destino)

    # Carrega as configurações da clínica correta
    config = carregar_configuracoes_clinica(clinic_id)

    # Gera a resposta usando a configuração da clínica
    resposta = responder_paciente(telefone, mensagem, config=config)

    # Envia a resposta pelo Twilio
    try:
        client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
        client.messages.create(
            body=resposta,
            from_=numero_destino,  # mantém o número original de destino
            to=telefone
        )
    except Exception as e:
        print(f"[ERRO] Falha ao enviar mensagem pelo Twilio: {e}")

    return "ok", 200