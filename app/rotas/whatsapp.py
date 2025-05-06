# ✅ whatsapp.py com controle de limite de caracteres (1600) e comentários explicativos

from flask import Blueprint, request
from app.utilitarios.extrair_nome import extrair_nome
from app.config.identidade_clinica import carregar_identidade_clinica
from app.utilitarios.configuracoes_clinica import carregar_configuracoes_clinica
from app.agentes.agente_memoria import agente_com_memoria  # Certifique-se que este nome está correto
from twilio.rest import Client
import os
import json

whatsapp = Blueprint("whatsapp", __name__)

# 🔍 Identifica a clínica a partir do número de destino

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

# 🚀 Webhook principal que recebe mensagens

@whatsapp.route("/webhook", methods=["POST"])
def webhook_whatsapp():
    telefone = request.form.get("From")
    mensagem = request.form.get("Body")
    numero_destino = request.form.get("To")

    if not telefone or not mensagem or not numero_destino:
        return "Requisição inválida", 400

    clinic_id = identificar_clinica_por_numero(numero_destino)
    carregar_identidade_clinica(clinic_id)

    # ⚙️ Detecta se é um JSON estruturado
    try:
        input_data = json.loads(mensagem)
        entrada_estruturada = (
            isinstance(input_data, dict)
            and "clinica_id" in input_data
            and "especialidade" in input_data
        )
    except json.JSONDecodeError:
        entrada_estruturada = False

    # 🎯 Prepara o prompt para o agente
    if entrada_estruturada:
        mensagem_para_agente = json.dumps(input_data)
    else:
        mensagem_para_agente = f"[clinica_id: {clinic_id}]\n{mensagem}"

    try:
        resposta = agente_com_memoria.invoke(
            {"input": mensagem_para_agente},
            config={"configurable": {"session_id": telefone}}
        )

        print(f"[INFO] Resposta gerada: {resposta}")

        # 💬 Trata mensagens longas para não exceder 1600 caracteres (limite do Twilio)
        mensagem_final = resposta if isinstance(resposta, str) else str(resposta)
        partes = [mensagem_final[i:i+1500] for i in range(0, len(mensagem_final), 1500)]

        client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
        for parte in partes:
            client.messages.create(
                body=parte,
                from_=numero_destino,
                to=telefone
            )

    except Exception as e:
        print(f"[ERRO] Falha no processamento ou envio: {e}")
        return "Erro interno", 500

    return "ok", 200
