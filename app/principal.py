from flask import Blueprint, request, jsonify
from app.utilitarios.extrair_nome import extrair_nome
from app.utilitarios.detectar_intencao import detectar_intencao_mensagem
from app.config.identidade_clinica import carregar_identidade_clinica
from app.agentes.agente_virtual import gerar_resposta

whatsapp = Blueprint("whatsapp", __name__)

@whatsapp.route("/webhook", methods=["POST"])
def receber_mensagem():
    try:
        dados = request.get_json()
        mensagem = dados.get("mensagem")
        telefone = dados.get("telefone")
        clinic_id = dados.get("clinic_id", "bemquerer")  # fallback padrão

        if not mensagem or not telefone:
            return jsonify({"erro": "mensagem e telefone são obrigatórios"}), 400

        # Carrega identidade da clínica
        identidade = carregar_identidade_clinica(clinic_id)

        # Detecta intenção e extrai nome
        nome_detectado = extrair_nome_paciente(mensagem)
        intencao = detectar_intencao_mensagem(mensagem)

        # Gera resposta usando o agente virtual
        resposta = gerar_resposta(
            mensagem_usuario=mensagem,
            identidade_clinica=identidade,
            telefone_usuario=telefone,
            nome_detectado=nome_detectado,
            intencao=intencao,
            clinic_id=clinic_id
        )

        return jsonify({
            "resposta": resposta,
            "intencao": intencao,
            "nome_detectado": nome_detectado,
            "clinica_id": clinic_id
        })

    except Exception as e:
        return jsonify({"erro": str(e)}), 500