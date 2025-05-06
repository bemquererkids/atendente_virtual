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

    return "bemquerer"  # fallback padrão

@whatsapp.route("/webhook", methods=["POST"])
def webhook_whatsapp():
    telefone = request.form.get("From")
    mensagem = request.form.get("Body")
    numero_destino = request.form.get("To")

    if not telefone or not mensagem or not numero_destino:
        return "Requisição inválida", 400

    # 🏥 Identifica a clínica
    clinic_id = identificar_clinica_por_numero(numero_destino)
    carregar_identidade_clinica(clinic_id)

    # 🧠 Opcional: extrai nome da mensagem
    nome_detectado = extrair_nome(mensagem)

    # 🔗 Injeta o clinic_id no contexto da mensagem
    mensagem_com_contexto = f'{{"clinica_id": "{clinic_id}", "mensagem": """{mensagem}"""}}'

    # 🤖 Invoca o agente com memória
    resposta = agente_com_memoria.invoke(
        {"input": mensagem_com_contexto},
        config={"configurable": {"session_id": telefone}}
    )

    resposta_texto = resposta.content if hasattr(resposta, "content") else str(resposta)
    print(f"[LOG] Resposta gerada: {resposta_texto}")

    try:
        client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
        client.messages.create(
            body=resposta_texto,
            from_=numero_destino,
            to=telefone
        )
    except Exception as e:
        print(f"[ERRO] Falha ao enviar mensagem pelo Twilio: {e}")

    return "ok", 200