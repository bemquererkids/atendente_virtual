# ✅ agente_memoria.py — Agente com suporte a Tools e memória de sessão

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain.agents import Tool, initialize_agent

from app.memoria.historico_redis import obter_historico_usuario
from app.tools.especialidade_tool import responder_especialidade

# ⚙️ Configuração do modelo de linguagem
llm = ChatOpenAI(model="gpt-4", temperature=0.3)

# 🧰 Lista de ferramentas (Tools) disponíveis
ferramentas = [
    Tool(
        name="responder_especialidade",
        func=responder_especialidade,
        description=(
            "Use esta ferramenta para responder perguntas sobre especialidades da clínica.\n"
            "Aceita perguntas em texto livre (ex: 'Vocês fazem implante?') ou em formato JSON com os campos:\n"
            "{'clinica_id': 'bemquerer', 'especialidade': 'implante'}"
        ),
    )
]

# 🧠 Prompt base com histórico da conversa
prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é uma secretária acolhedora e atenciosa de uma clínica odontológica."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# 🤖 Criação do agente com memória via Redis
# Usa um agente reativo com ferramentas e histórico de sessão
agente_com_memoria = RunnableWithMessageHistory(
    initialize_agent(
        tools=ferramentas,
        llm=llm,
        agent_type="chat-zero-shot-react-description",
        prompt=prompt,
        verbose=True,
        handle_parsing_errors=True
    ),
    get_session_history=lambda session_id: obter_historico_usuario(session_id),
    input_messages_key="input",
    history_messages_key="history"
)