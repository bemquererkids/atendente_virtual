# app/utilitarios/respostas_especialidades.py

from app.utilitarios.configuracoes_clinica import carregar_configuracoes_clinica

def responder_especialidade(pergunta: str, clinic_id: str = "bemquerer") -> str:
    pergunta = pergunta.lower()
    dados = carregar_configuracoes_clinica(clinic_id)
    especialidades = dados.get("especialidades", {})

    for chave, conteudo in especialidades.items():
        palavras_chave = conteudo.get("palavras_chave", [])
        for termo in palavras_chave:
            if termo.lower() in pergunta:
                return conteudo.get("resposta", "Temos atendimento nessa área. Quer que eu veja os horários disponíveis?")

    return "Temos atendimento especializado para diversas áreas. Pode me contar um pouquinho mais sobre sua dúvida ou necessidade?"