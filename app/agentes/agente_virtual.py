import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent
from langchain.schema import HumanMessage
from app.tools import tools

# Carrega variáveis do .env (opcional para ambientes locais)
load_dotenv()

def criar_agente_virtual():
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("❌ OPENAI_API_KEY não carregada. Verifique o .env ou Render.")

    llm = ChatOpenAI(openai_api_key=api_key, temperature=0.7)

    return initialize_agent(
        tools=tools,
        llm=llm,
        agent="chat-conversational-react-description",
        verbose=True
    )

def gerar_resposta(
    mensagem_usuario: str,
    identidade_clinica: dict,
    telefone_usuario: str,
    nome_detectado: str = None,
    intencao: str = None,
    clinic_id: str = None
) -> str:
    """
    Gera uma resposta personalizada usando o agente LLM e o contexto da clínica.

    Parâmetros:
    - mensagem_usuario: mensagem recebida
    - identidade_clinica: dict com os dados da clínica (nome, estilo, etc.)
    - telefone_usuario: número de telefone do paciente
    - nome_detectado: nome extraído (opcional)
    - intencao: intenção detectada (opcional)
    - clinic_id: identificador da clínica (opcional)

    Retorna:
    - Texto da resposta gerada
    """
    agente = criar_agente_virtual()

    contexto = (
        f"Você é a secretária virtual da clínica {identidade_clinica.get('nome_clinica')}.\n"
        f"Estilo de comunicação: {identidade_clinica.get('estilo_comunicacao')}.\n"
        f"Nível de formalidade: {identidade_clinica.get('nivel_formalidade')}.\n"
        f"Dores do paciente: {identidade_clinica.get('dores_pacientes')}.\n"
        f"Apresente-se como {identidade_clinica.get('nome_secretaria')} e aja com empatia e clareza.\n"
    )

    prompt = (
        f"{contexto}\n"
        f"Mensagem recebida: '{mensagem_usuario}'\n"
    )

    if nome_detectado:
        prompt += f"Nome do paciente: {nome_detectado}\n"
    if intencao:
        prompt += f"Intenção identificada: {intencao}\n"
    if clinic_id:
        prompt += f"ID da clínica: {clinic_id}\n"

    try:
        resposta = agente.run(HumanMessage(content=prompt))
        return resposta.strip()
    except Exception as e:
        print(f"[ERRO] Falha ao gerar resposta com agente virtual: {e}")
        return "Tivemos uma instabilidade. Pode me enviar a mensagem novamente, por favor?"