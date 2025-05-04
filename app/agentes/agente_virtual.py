import os
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent
from app.tools import tools

def criar_agente_virtual():
    from dotenv import load_dotenv
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("❌ OPENAI_API_KEY não foi carregada. Verifique o .env ou variáveis no Render.")

    llm = ChatOpenAI(openai_api_key=api_key, temperature=0.7)

    return initialize_agent(
        tools=tools,
        llm=llm,
        agent="chat-conversational-react-description",
        verbose=True
    )