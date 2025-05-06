# ✅ agente_memoria.py — Agente com suporte a Tools e memória de sessão
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain.agents import Tool, initialize_agent

from app.memoria.historico_redis import obter_historico_usuario
from app.tools.especialidade_tool import responder_especialidade

# ⚙️ Configuração do modelo de linguagem
llm = ChatOpenAI(model="gpt-4", temperature=0.3)

# 🧰 Lista de ferramentas disponíveis
ferramentas = [
    Tool(
        name="responder_especialidade",
        func=responder_especialidade,
        description=(
            "Use esta ferramenta para responder perguntas sobre especialidades da clínica.\n"
            "Aceita perguntas em texto livre ou em formato JSON com os campos 'clinica_id' e 'especialidade'."
        ),
    )
]

# 🧠 Prompt que define o comportamento e mantém o histórico da conversa
prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é uma secretária acolhedora e atenciosa de uma clínica odontológica."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# 🤖 Agente com memória e suporte a tools
agente_executor = initialize_agent(
    tools=ferramentas,
    llm=llm,
    agent_type="chat-zero-shot-react-description",
    verbose=True,
    handle_parsing_errors=True
)

# ⏳ Executor com memória
agente_com_memoria = RunnableWithMessageHistory(
    agente_executor,
    get_session_history=lambda session_id: obter_historico_usuario(session_id),
    input_messages_key="input",
    history_messages_key="history"
)