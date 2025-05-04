from app.tools.prompt_loader import carregar_prompts_padrao
from app.config.identidade_secretaria import config_clinica
from app.utilitarios.chatgpt import gerar_resposta_informativa
from app.tools.faq_tool import buscar_faq_func

prompts = carregar_prompts_padrao()

def preencher_variaveis(prompt: str, especialidade_slug: str = "", nome_usuario: str = "") -> str:
    especialista = config_clinica.get("especialistas", {}).get(especialidade_slug, {})
    agenda = config_clinica.get("agenda_disponivel", {}).get(especialidade_slug, {})

    nome_profissional = especialista.get("nome", "nossa equipe")
    especialidade = especialista.get("especialidade", especialidade_slug or "nosso atendimento")
    
    dias = agenda.get(nome_profissional)
    disponibilidade = ", ".join(dias) if dias else "em dias flexíveis"

    prompt = prompt.replace("{{NOME_CLINICA}}", config_clinica.get("nome", "a clínica"))
    prompt = prompt.replace("{{nome}}", nome_usuario or "você")
    prompt = prompt.replace("{{PROFISSIONAL}}", nome_profissional)
    prompt = prompt.replace("{{ESPECIALIDADE}}", especialidade)
    prompt = prompt.replace("{{DISPONIBILIDADE}}", disponibilidade)

    return prompt

def gerar_resposta_por_intencao(intencao, mensagem_usuario="", nome_usuario=""):
    if intencao == "faq":
        return buscar_faq_func(
            pergunta_usuario=mensagem_usuario,
            clinic_id=config_clinica.get("clinica_id", "bemquerer_odontologia")
        )

    elif intencao in ["consulta_rotina", "checkup", "prevenção"]:
        return preencher_variaveis(prompts.get("consulta_rotina", ""), "odontopediatria", nome_usuario)

    elif intencao in ["dor", "urgencia", "emergencia"]:
        return preencher_variaveis(prompts.get("dor", ""), "clinico_geral", nome_usuario)

    elif intencao in ["retorno", "continuidade", "acompanhar"]:
        return preencher_variaveis(prompts.get("retorno", ""), "", nome_usuario)

    elif intencao in ["preco", "valor", "investimento"]:
        return preencher_variaveis(prompts.get("preco", ""), "", nome_usuario)

    elif intencao in ["especialidade", "interesse_servico", "tratamento"]:
        return preencher_variaveis(prompts.get("especialidade", ""), "ortodontia", nome_usuario)

    elif intencao in ["atendimento_especial", "tea", "síndrome", "autismo", "pne"]:
        return preencher_variaveis(prompts.get("agendamento_especial", ""), "odontopediatria", nome_usuario)

    elif intencao in ["sedacao", "sedação", "anestesia", "medo"]:
        return preencher_variaveis(prompts.get("sedacao", ""), "sedacao", nome_usuario)

    elif intencao in ["invisalign", "aparelho invisivel", "alinhador"]:
        return preencher_variaveis(prompts.get("invisalign", ""), "invisalign", nome_usuario)

    elif intencao in ["implante", "falta dente", "perdi o dente"]:
        return preencher_variaveis(prompts.get("implante", ""), "implante", nome_usuario)

    # fallback: se nenhuma intenção for tratada
    prompt = prompts.get("fallback", "")
    if prompt:
        return preencher_variaveis(prompt, "", nome_usuario)

    # fallback final com GPT (reforço via agente)
    return gerar_resposta_informativa(mensagem_usuario, nome=nome_usuario)