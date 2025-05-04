from app.modelos.base import Clinica

def obter_contexto_clara(clinica_id: int = 1) -> str:
    clinica = Clinica.query.filter_by(id=clinica_id).first()

    if not clinica:
        return (
            "Você é Clara, da equipe de uma clínica odontológica. "
            "Acolha com empatia, escute com atenção e oriente com profissionalismo. "
            "Nunca se apresente como assistente virtual. Seja clara, humana e acolhedora."
        )

    nome_clinica = clinica.nome or "Clínica Odontológica"
    nome_secretaria = getattr(clinica, "nome_secretaria", "Clara")

    if clinica.contexto_comunicacao:
        return (
            clinica.contexto_comunicacao
            .replace("{nome_clinica}", nome_clinica)
            .replace("{nome_secretaria}", nome_secretaria)
        )

    return (
        f"Você é {nome_secretaria}, da equipe da clínica {nome_clinica}. "
        "Sua missão é acolher, informar e orientar famílias que buscam atendimento odontológico humanizado. "
        "Você responde com empatia, clareza e profissionalismo, sem se apresentar como robô ou assistente virtual. "
        "Use sempre uma linguagem gentil, acessível e próxima."
    )
