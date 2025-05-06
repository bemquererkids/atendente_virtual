# ✅ agente_virtual.py atualizado com suporte a Tool estruturada e entrada como texto

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain.agents import Tool, initialize_agent
from app.memoria.historico_redis import obter_historico_usuario
from app.tools.especialidade_tool import responder_especialidade

# ⚙️ Configuração do LLM
llm = ChatOpenAI(model="gpt-4", temperature=0.3)

# 🧰 Ferramentas disponíveis
ferramentas = [
    Tool(
        name="responder_especialidade",
        func=responder_especialidade,
        description=(
            "Use esta ferramenta para responder perguntas sobre especialidades da clínica. "
            "Aceita uma string do usuário contendo a especialidade e o identificador da clínica como [clinica_id: bemquerer]."
        ),
    )
]

# 🧠 Prompt com histórico de conversa
prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é uma secretária acolhedora e eficiente de uma clínica odontológica."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# 🤖 Agente com memória de sessão
agente_base = initialize_agent(
    tools=ferramentas,
    llm=llm,
    agent_type="chat-zero-shot-react-description",
    verbose=True,
    handle_parsing_errors=True,
    return_intermediate_steps=False
)

agente_com_memoria = RunnableWithMessageHistory(
    agente_base,
    lambda session_id: obter_historico_usuario(session_id),
    input_messages_key="input",
    history_messages_key="history"
)
