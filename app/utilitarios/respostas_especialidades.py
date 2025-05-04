# app/utilitarios/respostas_especialidades.py

from app.utilitarios.configuracoes_clinica import carregar_config

def responder_especialidade(pergunta: str) -> str:
    pergunta = pergunta.lower()
    dados = carregar_config()
    especialidades = dados.get("especialidades", {})

    for chave, conteudo in especialidades.items():
        palavras_chave = conteudo.get("palavras_chave", [])
        for termo in palavras_chave:
            if termo.lower() in pergunta:
                return conteudo.get("resposta", "Temos atendimento nessa área. Quer que eu veja os horários disponíveis?")

    return "Temos atendimento especializado para diversas áreas. Pode me contar um pouquinho mais sobre sua dúvida ou necessidade?"