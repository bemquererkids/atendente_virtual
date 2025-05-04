from datetime import datetime
from pytz import timezone
from app.modelos.base import Clinica, Contexto, banco
from app.utilitarios.chatgpt import interpretar_intencao_com_chatgpt, gerar_resposta_informativa

# 🔹 Classificador de intenção

def classificar_intencao(mensagem: str) -> str:
    mensagem = mensagem.lower()
    if any(p in mensagem for p in ["preço", "valor", "quanto", "custa"]):
        return "valores"
    elif any(p in mensagem for p in ["horário", "agenda", "sábado", "atendem que horas"]):
        return "agenda"
    elif any(p in mensagem for p in ["dor", "incomodo", "urgência", "urgente"]):
        return "dor"
    elif any(p in mensagem for p in ["tea", "autismo", "especial", "síndrome"]):
        return "atendimento para TEA ou necessidades especiais"
    elif any(p in mensagem for p in ["alinhador", "invisalign", "aparelho", "ortodontia"]):
        return "tratamento ortodôntico"
    elif any(p in mensagem for p in ["lente", "prótese", "implante"]):
        return "estética ou reabilitação"
    else:
        return "algum atendimento"

# 🔹 Detectar intenção espontânea

def detectar_intencao_espontanea(mensagem: str) -> str:
    mensagem = mensagem.lower()
    if any(p in mensagem for p in ["prótese", "implante", "lente"]):
        return "prótese"
    if any(p in mensagem for p in ["canal", "tratamento de canal"]):
        return "tratamento de canal"
    if any(p in mensagem for p in ["dor", "urgência", "emergência"]):
        return "urgência"
    if any(p in mensagem for p in ["alinhador", "aparelho", "invisalign"]):
        return "ortodontia"
    if any(p in mensagem for p in ["criança", "tea", "autismo", "especial"]):
        return "odontopediatria"
    return ""

# 🔹 Saudação inicial com acolhimento natural

from datetime import datetime
from pytz import timezone
from app.modelos.base import Clinica, Contexto, banco

# 🔹 Saudação inicial acolhedora

def saudacao_com_escuta(numero: str, mensagem_usuario: str, clinica_id: int = 1) -> str:
    clinica = Clinica.query.filter_by(id=clinica_id).first()
    nome_clinica = clinica.nome
    nome_secretaria = clinica.nome_secretaria or "Clara"

    fuso_brasilia = timezone('America/Sao_Paulo')
    hora = datetime.now(fuso_brasilia).hour
    saudacao = "Bom dia" if hora < 12 else "Boa tarde" if hora < 18 else "Boa noite"

    contexto = Contexto.query.filter_by(telefone_usuario=numero).first()
    agora = datetime.now(fuso_brasilia)

    if contexto:
        contexto.ultima_interacao = mensagem_usuario
        contexto.ultima_resposta = "Início de conversa"
        contexto.atualizado_em = agora
        contexto.etapa = "solicitar_nome"
    else:
        contexto = Contexto(
            telefone_usuario=numero,
            ultima_interacao=mensagem_usuario,
            ultima_resposta="Início de conversa",
            criado_em=agora,
            atualizado_em=agora,
            etapa="solicitar_nome"
        )
        banco.session.add(contexto)

    banco.session.commit()

    return f"{saudacao}! 🌻 Eu sou {nome_secretaria}, secretária da clínica {nome_clinica}. Com quem eu tenho o prazer de falar?"




# 🔹 Interpretação de resposta inicial e fluxo completo

def interpretar_resposta_inicial(numero: str, mensagem_usuario: str) -> str:
    mensagem = mensagem_usuario.strip()
    mensagem_lower = mensagem.lower()
    contexto = Contexto.query.filter_by(telefone_usuario=numero).first()

    if not contexto:
        return "Antes de tudo, posso saber com quem eu falo?"

    if contexto.etapa == "aguardar_nome_inicial":
        palavras = mensagem.split()

        # 🔥 Nova inteligência: se parece dúvida ou pergunta, acolhe com GPT imediatamente
        if (
            "?" in mensagem_lower
            or len(palavras) > 3
            or any(p in mensagem_lower for p in ["fazem", "atendem", "tem", "vocês", "consulta", "atendimento", "urgência", "dor", "autismo", "especial", "sedação", "anestesia"])
        ):
            resposta = gerar_resposta_informativa(mensagem_usuario)
            contexto.ultima_interacao = mensagem_usuario
            contexto.ultima_resposta = resposta
            contexto.atualizado_em = datetime.now(timezone('America/Sao_Paulo'))
            banco.session.commit()
            return f"{resposta}\n\nSó para seguirmos melhor, com quem eu tenho o prazer de falar?"

        # Se é nome curto, registra normalmente
        contexto.nome = mensagem.title()
        contexto.etapa = "aguardar_intencao"
        banco.session.commit()
        return f"Que bom falar com você, {contexto.nome}! Em que posso te ajudar hoje?"

    if contexto.etapa == "aguardar_intencao":
        intencao = detectar_intencao_espontanea(mensagem_lower)

        if not intencao:
            intencao = interpretar_intencao_com_chatgpt(mensagem_lower)

        if intencao:
            contexto.motivo = intencao

        resposta_informativa = gerar_resposta_informativa(mensagem_usuario)

        contexto.etapa = "verificar_responsavel"
        banco.session.commit()

        if resposta_informativa:
            return resposta_informativa + "\n\nPra quem seria a consulta? Pra você mesmo ou para um filho(a)/familiar?"
        else:
            return "Nossa equipe é especializada em atender todas as necessidades com muito carinho e profissionalismo 🌻.\n\nPra quem seria a consulta? Pra você mesmo ou para um filho(a)/familiar?"

    # 🔥 As demais etapas seguem normalmente...





    if contexto.etapa == "verificar_responsavel":
        if any(p in mensagem for p in ["filho", "filha", "criança", "menino", "menina", "sobrinho", "sobrinha"]):
            contexto.tipo_paciente = "criança"
            contexto.etapa = "nome_paciente"
            banco.session.commit()
            return "Qual o nome da criança?"
        elif any(p in mensagem for p in ["eu", "pra mim", "para mim", "meu", "minha", "adulto"]):
            contexto.tipo_paciente = "adulto"
            contexto.etapa = "nome_paciente"
            banco.session.commit()
            return "Qual o seu nome, por favor?"
        else:
            contexto.etapa = "nome_paciente"
            banco.session.commit()
            return "Entendi! Pode me informar o nome da pessoa que vai ser atendida?"

    if contexto.etapa == "nome_paciente":
        contexto.nome = mensagem_usuario.strip().title()
        if contexto.tipo_paciente == "criança":
            contexto.etapa = "idade_paciente"
            banco.session.commit()
            return f"Quantos anos tem {contexto.nome}?"
        else:
            contexto.etapa = "detectar_intencao"
            banco.session.commit()
            return f"{contexto.nome}, você está com alguma dor ou incômodo agora?"

    if contexto.etapa == "idade_paciente":
        if contexto.dados is None:
            contexto.dados = {}
        contexto.dados["idade"] = mensagem_usuario.strip()
        contexto.etapa = "vinculo_responsavel"
        banco.session.commit()
        return f"Você é o(a) responsável direto por {contexto.nome}? Pai, mãe ou cuidador(a)?"

    if contexto.etapa == "vinculo_responsavel":
        contexto.dados["vinculo"] = mensagem_usuario.strip().lower()
        contexto.etapa = "detectar_intencao"
        banco.session.commit()
        return f"{contexto.nome} está com alguma dor ou incômodo agora?"

    if contexto.etapa == "detectar_intencao":
        intencao = detectar_intencao_espontanea(mensagem)
        if intencao:
            contexto.motivo = intencao
            contexto.etapa = "origem"
            banco.session.commit()
            return f"Perfeito! Já anotei aqui: {intencao}. Você já conhece a clínica ou veio por indicação de alguém?"
        else:
            contexto.etapa = "tipo_consulta"
            banco.session.commit()
            return "Você está buscando uma consulta de rotina, urgência ou emergência?"

    if contexto.etapa == "tipo_consulta":
        if "rotina" in mensagem or "eletiva" in mensagem:
            contexto.motivo = "eletiva"
        elif "urgência" in mensagem:
            contexto.motivo = "urgência"
        elif "emergência" in mensagem:
            contexto.motivo = "emergência"
        else:
            contexto.motivo = "não informado"
        contexto.etapa = "origem"
        banco.session.commit()
        return "Você já conhece a clínica ou veio por indicação de alguém?"

    if contexto.etapa == "origem":
        if contexto.dados is None:
            contexto.dados = {}
        if any(p in mensagem for p in ["indicação", "indicado", "jaat"]):
            contexto.dados["origem"] = "indicação"
        elif "instagram" in mensagem:
            contexto.dados["origem"] = "instagram"
        elif "google" in mensagem:
            contexto.dados["origem"] = "google"
        elif any(p in mensagem for p in ["sou paciente", "já sou"]):
            contexto.dados["origem"] = "paciente da casa"
        else:
            contexto.dados["origem"] = "não informado"
        contexto.etapa = "finalizado"
        banco.session.commit()
        return "Obrigada pelas informações! Agora já consigo te direcionar para o melhor atendimento 💙 Aguarde um instantinho."

    return "As informações estão todas registradas. Em breve seguimos com o melhor direcionamento!"
