from app.modelos.base import banco, Clinica
from app.principal import criar_aplicacao

app = criar_aplicacao()

with app.app_context():
    clinica = Clinica.query.filter_by(id=1).first()

    if clinica:
        print("🔄 Clínica encontrada. Atualizando dados...")
        clinica.nome = "Bem-Querer Odontologia"
        clinica.cidade = "Santo André"
        clinica.nome_secretaria = "Clara"
        clinica.contexto_comunicacao = """
Você é {nome_secretaria}, da equipe da clínica {nome_clinica}.
Sua missão é acolher, informar e orientar famílias que buscam atendimento odontológico humanizado.

Você responde com empatia, clareza e profissionalismo, sem se apresentar como robô ou assistente virtual.
Use sempre uma linguagem gentil, acessível e próxima.
"""
    else:
        print("➕ Clínica não encontrada. Criando nova entrada...")
        clinica = Clinica(
            id=1,
            nome="Bem-Querer Odontologia",
            cidade="Santo André",
            nome_secretaria="Clara",
            contexto_comunicacao="""
Você é {nome_secretaria}, da equipe da clínica {nome_clinica}.
Sua missão é acolher, informar e orientar famílias que buscam atendimento odontológico humanizado.

Você responde com empatia, clareza e profissionalismo, sem se apresentar como robô ou assistente virtual.
Use sempre uma linguagem gentil, acessível e próxima.
"""
        )
        banco.session.add(clinica)

    banco.session.commit()
    print("✅ Dados da clínica ajustados com sucesso.")
