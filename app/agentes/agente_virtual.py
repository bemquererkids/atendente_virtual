# ✅ agente_virtual.py atualizado com suporte a Tool estruturada

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from app.memoria.historico_redis import obter_historico_usuario
from app.tools.especialidade_tool import responder_especialidade
from langchain.agents import Tool, initialize_agent

# ⚙️ Configuração do LLM
llm = ChatOpenAI(model="gpt-4", temperature=0.3)

# 📌 Ferramentas disponíveis
ferramentas = [
    Tool(
        name="responder_especialidade",
        func=responder_especialidade,
        description="Fornece informações detalhadas sobre especialidades da clínica. Requer 'clinica_id' e o nome da especialidade."
    )
]

# 🧠 Prompt com histórico e input
prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é uma secretária atenciosa e acolhedora de uma clínica odontológica."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# 🤖 Agente com memória
agente_com_memoria = RunnableWithMessageHistory(
    initialize_agent(
        tools=ferramentas,
        llm=llm,
        agent_type="chat-zero-shot-react-description",
        verbose=True,
        handle_parsing_errors=True
    ),
    lambda session_id: obter_historico_usuario(session_id),
    input_messages_key="input",
    history_messages_key="history"
)
