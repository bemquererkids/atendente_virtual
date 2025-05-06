# ✅ agente_memoria.py - agente com memória e tool de especialidades

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain.agents import Tool, initialize_agent
from app.memoria.historico_redis import obter_historico_usuario
from app.tools.especialidade_tool import responder_especialidade

# ⚙️ Configuração do modelo de linguagem
llm = ChatOpenAI(model="gpt-4", temperature=0.3)

# 🛠️ Definição da ferramenta de especialidades
ferramentas = [
    Tool(
        name="responder_especialidade",
        func=responder_especialidade,
        description=(
            "Use esta ferramenta para responder perguntas sobre especialidades da clínica.\n"
            "Aceita mensagens com JSON ou texto contendo o identificador da clínica.\n"
            "Exemplo válido de JSON: {'clinica_id': 'bemquerer', 'especialidade': 'implante'}"
        ),
    )
]

# 🧠 Prompt base com histórico
prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é uma secretária acolhedora, clara e prestativa de uma clínica odontológica."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# 🤖 Agente com histórico via Redis e ferramentas
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
