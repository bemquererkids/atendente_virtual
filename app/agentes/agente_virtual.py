import os
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent
from app.tools import tools
from app.utilitarios.configuracoes_clinica import carregar_configuracoes_clinica

def criar_agente_virtual(clinic_id="bemquerer"):
    """
    Cria um agente virtual LangChain com base na configuração da clínica.
    """
    from dotenv import load_dotenv
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("❌ OPENAI_API_KEY não foi carregada. Verifique o .env ou variáveis no Render.")

    # Carrega configurações específicas da clínica
    config = carregar_configuracoes_clinica(clinic_id)

    # Define temperatura personalizada se existir
    temperatura = config.get("temperatura_modelo", 0.7)

    llm = ChatOpenAI(
        openai_api_key=api_key,
        temperature=temperatura
    )

    # Inicializa o agente com as ferramentas e LLM
    return initialize_agent(
        tools=tools,
        llm=llm,
        agent="chat-conversational-react-description",
        verbose=True
    )