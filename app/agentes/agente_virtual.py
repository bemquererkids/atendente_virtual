# app/agentes/agente_virtual.py

from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.memoria.historico_redis import obter_historico_usuario
import os

# 1. Modelo base OpenAI
modelo_llm = ChatOpenAI(temperature=0.3)

# 2. Template de conversa com placeholders
prompt = ChatPromptTemplate.from_messages([
    ("system", """
        Você é uma secretária humanizada de uma clínica odontológica. 
        Seu papel é acolher o paciente, entender a necessidade dele 
        e conduzir a conversa com leveza, cuidado e clareza.
        Nunca se identifique como assistente virtual.
    """),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{mensagem}")
])

# 3. Cadeia básica de resposta (LLM + Prompt)
cadeia_resposta = prompt | modelo_llm

# 4. Envoltório com memória Redis (mantém histórico por telefone)
agente_com_memoria = RunnableWithMessageHistory(
    cadeia_resposta,
    lambda session_id: obter_historico_usuario(session_id),
    input_messages_key="mensagem",
    history_messages_key="history"
)
