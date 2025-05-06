# ✅ agente_memoria.py — agente com memória e entrada via "input" padrão
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain.agents import Tool, initialize_agent
from app.memoria.historico_redis import obter_historico_usuario
from app.tools.especialidade_tool import responder_especialidade

# 🔧 LLM configurado com temperatura baixa para consistência
llm = ChatOpenAI(model="gpt-4", temperature=0.3)

# 📦 Tool única — responder especialidade com JSON ou texto livre
ferramentas = [
    Tool(
        name="responder_especialidade",
        func=responder_especialidade,
        description=(
            "Use esta ferramenta para responder perguntas sobre especialidades da clínica.\n"
            "Aceita: {'clinica_id': 'bemquerer', 'especialidade': 'implante'} ou texto com [clinica_id: bemquerer]"
        )
    )
]

# 📜 Prompt com histórico de conversa e chave 'input'
prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é uma secretária atenciosa e acolhedora de uma clínica odontológica."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# 🧠 Agente com memória (Redis) e entrada padronizada
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