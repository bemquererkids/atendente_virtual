# 📁 app/rotas/whatsapp.py

from flask import Blueprint, request
from app.utilitarios.extrair_nome import extrair_nome
from app.config.identidade_clinica import carregar_identidade_clinica
from app.utilitarios.configuracoes_clinica import carregar_configuracoes_clinica
from app.agentes.agente_memoria import agente_com_memoria  # ✅ Importa o agente correto com memória
from twilio.rest import Client
import os
import json

# 🟦 Blueprint do WhatsApp para registrar rotas relacionadas
whatsapp = Blueprint("whatsapp", __name__)

# 🔎 Identifica a clínica com base no número do WhatsApp de destino (ex: para multiclinica)
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

    return "bemquerer"  # 🔁 fallback para uma clínica padrão

# 📩 Rota principal que lida com mensagens recebidas via WhatsApp
@whatsapp.route("/webhook", methods=["POST"])
def webhook_whatsapp():
    telefone = request.form.get("From")
    mensagem = request.form.get("Body")
    numero_destino = request.form.get("To")

    if not telefone or not mensagem or not numero_destino:
        return "Requisição inválida", 400

    # 🏥 Identifica a clínica com base no número do destinatário
    clinic_id = identificar_clinica_por_numero(numero_destino)

    # 🔧 Carrega configurações e identidade da clínica
    carregar_identidade_clinica(clinic_id)
    carregar_configuracoes_clinica(clinic_id)

    # ✅ Verifica se a mensagem é um JSON com campos estruturados
    try:
        input_data = json.loads(mensagem)
        if isinstance(input_data, dict) and "clinica_id" in input_data and "especialidade" in input_data:
            entrada_estruturada = True
        else:
            entrada_estruturada = False
    except json.JSONDecodeError:
        entrada_estruturada = False

    # 🧠 Prepara a entrada a ser enviada para o agente (com ou sem contexto embutido)
    if entrada_estruturada:
        mensagem_para_agente = json.dumps(input_data)
    else:
        mensagem_para_agente = f"[clinica_id: {clinic_id}]\n{mensagem}"

    try:
        # 🤖 Envia para o agente com memória
        resposta = agente_com_memoria.invoke(
            {"input": mensagem_para_agente},
            config={"configurable": {"session_id": telefone}}
        )

        print(f"[INFO] Resposta gerada: {resposta}")

        # 📤 Envia a resposta de volta via Twilio
        client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
        client.messages.create(
            body=resposta if isinstance(resposta, str) else str(resposta),
            from_=numero_destino,
            to=telefone
        )

    except Exception as e:
        print(f"[ERRO] Falha no processamento ou envio: {e}")
        return "Erro interno", 500

    return "ok", 200