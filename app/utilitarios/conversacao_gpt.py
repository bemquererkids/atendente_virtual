# app/utilitarios/conversacao_gpt.py

from datetime import datetime
from app.modelos.base import banco, Contexto, HistoricoConversa
from app.utilitarios.extrair_nome import extrair_nome
from app.utilitarios.respostas_especialidades import responder_especialidade
from app.tools.intencao_router import gerar_resposta_por_intencao
from app.utilitarios.detectar_intencao import detectar_intencao_basica
from app.agentes.agente_virtual import criar_agente_virtual
from langchain.schema import HumanMessage, AIMessage

agente = criar_agente_virtual()

def interpretar_variaveis_ocultas(texto: str, contexto):
    intencao = detectar_intencao_basica(texto)
    texto = texto.lower()

    if any(p in texto for p in ["filho", "filha", "criança"]):
        contexto.tipo_paciente = "crianca"
    elif any(p in texto for p in ["eu", "adulto", "sou eu"]):
        contexto.tipo_paciente = "adulto"

    if "anos" in texto:
        contexto.dados["possivel_idade"] = texto

    if intencao == "atendimento_especial":
        contexto.dados["tipo_paciente"] = "especial"
    elif intencao == "dor":
        contexto.dados["possivel_dor"] = True

    return intencao

def responder_paciente(telefone: str, mensagem_usuario: str, config: dict) -> str:
    agora = datetime.now()
    clinic_id = config.get("clinica_id", "bemquerer")  # garante fallback

    contexto = Contexto.query.filter_by(telefone_usuario=telefone).first()
    if not contexto:
        contexto = Contexto(
            telefone_usuario=telefone,
            ultima_interacao=mensagem_usuario,
            criado_em=agora,
            atualizado_em=agora,
            etapa="saudacao",
            dados={}
        )
        banco.session.add(contexto)

    contexto.ultima_interacao = mensagem_usuario
    contexto.atualizado_em = agora
    banco.session.commit()

    nome = contexto.nome or ""
    dados = contexto.dados or {}

    intencao_detectada = interpretar_variaveis_ocultas(mensagem_usuario, contexto)
    banco.session.commit()

    if contexto.etapa == "saudacao":
        contexto.etapa = "coletar_nome"
        banco.session.commit()
        resposta = config.get("mensagem_abertura", f"Olá! Sou Clara, secretária da {config.get('nome_clinica', 'clínica')}. Com quem eu tenho o prazer de falar?")

    elif contexto.etapa == "coletar_nome":
        contexto.nome = extrair_nome(mensagem_usuario)
        contexto.etapa = "identificar_paciente"
        banco.session.commit()
        resposta = f"Que alegria te receber por aqui, {contexto.nome}! A consulta seria para você ou para outra pessoa (como filho(a), responsável, etc.)?"

    elif contexto.etapa == "identificar_paciente":
        texto = mensagem_usuario.lower()
        if any(p in texto for p in ["filho", "filha", "criança", "meu", "minha"]):
            contexto.tipo_paciente = "crianca"
            contexto.etapa = "dados_crianca"
            banco.session.commit()
            resposta = "Perfeito! Qual o nome da criança?"
        elif any(p in texto for p in ["eu", "adulto", "sou eu"]):
            contexto.tipo_paciente = "adulto"
            contexto.etapa = "investigar_queixa"
            banco.session.commit()
            resposta = f"Entendi, {contexto.nome}. Está com dor, desconforto, ou seria uma consulta de rotina mesmo?"
        else:
            resposta = "Só para confirmar: o atendimento é para você ou para outra pessoa?"

    elif contexto.etapa == "dados_crianca":
        contexto.dados["nome_crianca"] = extrair_nome(mensagem_usuario)
        contexto.etapa = "investigar_queixa"
        banco.session.commit()
        resposta = "Quantos anos tem a criança? Está com dor ou algum incômodo no momento?"

    elif contexto.etapa == "investigar_queixa":
        contexto.motivo = mensagem_usuario.strip()

        if intencao_detectada == "especialidade":
            resposta = responder_especialidade(mensagem_usuario, clinic_id=clinic_id)
        else:
            resposta = gerar_resposta_por_intencao(intencao_detectada, mensagem_usuario, contexto.nome or "Paciente")

        contexto.etapa = "agendamento"
        banco.session.commit()

    elif contexto.etapa == "agendamento":
        especialistas = config.get("agenda_disponivel", {}).get("odontopediatria", {})
        if especialistas:
            linhas = [f"{nome}: {', '.join(dias)}" for nome, dias in especialistas.items()]
            resposta = (
                "Temos disponibilidade com nossas odontopediatras nos seguintes dias:\n\n"
                + "\n".join(linhas)
                + "\n\nQual profissional ou dia você prefere?"
            )
        else:
            resposta = "Posso verificar os horários disponíveis com nossa equipe de odontopediatria. Você tem preferência por algum dia da semana ou profissional?"
        contexto.etapa = "finalizado"
        banco.session.commit()

    else:
        try:
            historico = HistoricoConversa.query.filter_by(telefone_usuario=telefone).order_by(HistoricoConversa.id.asc()).all()

            chat_history = []
            for item in historico[-5:]:
                chat_history.append(HumanMessage(content=item.mensagem))
                chat_history.append(AIMessage(content=item.resposta))

            resposta = agente.run({
                "input": mensagem_usuario,
                "chat_history": chat_history
            })
        except Exception as e:
            print(f"[ERRO] ao usar agente LangChain: {e}")
            resposta = config.get("mensagem_padrao_falha", "Estou aqui para te acolher! Se puder repetir ou me explicar melhor, fico feliz em continuar.")

    try:
        historico = HistoricoConversa(
            telefone_usuario=telefone,
            mensagem=mensagem_usuario,
            resposta=resposta
        )
        banco.session.add(historico)
        banco.session.commit()
    except Exception as e:
        print(f"[ERRO] Falha ao salvar histórico: {e}")

    return resposta