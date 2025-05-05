# app/agentes/agente_virtual.py

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnableMap
from langchain_openai import ChatOpenAI

from app.memoria.historico_redis import memory
from app.config.identidade_clinica import carregar_identidade_clinica

from langchain_core.messages import HumanMessage

# ⚙️ Modelo com temperatura controlada
modelo = ChatOpenAI(model="gpt-4", temperature=0.3)

# 🎯 Prompt com histórico
prompt = ChatPromptTemplate.from_messages([
    ("system", "{identidade}"),
    MessagesPlaceholder(variable_name="historico"),
    ("human", "{mensagem}")
])

# 🔗 Pipeline de execução
cadeia = prompt | modelo

# 🧠 Memória com Redis
agente_com_memoria = RunnableWithMessageHistory(
    cadeia,
    memory,
    input_messages_key="mensagem",
    history_messages_key="historico",
)

# 🚀 Função principal que pode ser chamada no webhook
def responder_paciente(mensagem: str, telefone: str, clinic_id: str = "bemquerer") -> str:
    identidade = carregar_identidade_clinica(clinic_id)

    resposta = agente_com_memoria.invoke(
        {
            "mensagem": mensagem,
            "identidade": identidade
        },
        config={"configurable": {"session_id": telefone}}
    )

    return resposta.content