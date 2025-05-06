# 📁 app/agentes/agente_memoria.py

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain.agents import Tool, initialize_agent
from app.memoria.historico_redis import obter_historico_usuario
from app.tools.especialidade_tool import responder_especialidade

# ⚙️ Inicializa o modelo da OpenAI com temperatura baixa para mais consistência nas respostas
llm = ChatOpenAI(model="gpt-4", temperature=0.3)

# 🛠️ Lista de ferramentas disponíveis para o agente (por enquanto, apenas especialidades)
ferramentas = [
    Tool(
        name="responder_especialidade",
        func=responder_especialidade,
        description=(
            "Usar quando a pessoa quiser saber se a clínica tem uma especialidade, o profissional que atende, "
            "e os diferenciais. Funciona com frase livre, desde que contenha algo como [clinica_id: bemquerer]."
        ),
    )
]

# 🧠 Template de prompt com histórico de conversa (mantém contexto entre mensagens)
prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é uma secretária humanizada de uma clínica odontológica, pronta para acolher e informar."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# 🤖 Configuração do agente com memória de sessão via Redis
agente_com_memoria = RunnableWithMessageHistory(
    initialize_agent(
        tools=ferramentas,
        llm=llm,
        agent_type="chat-zero-shot-react-description",  # 🧠 Usa RAG zero-shot com descrição de tools
        verbose=True,
        handle_parsing_errors=True  # ⚠️ Evita falha total caso o modelo retorne erro de parsing
    ),
    lambda session_id: obter_historico_usuario(session_id),
    input_messages_key="input",   # 🔑 Campo da mensagem de entrada
    history_messages_key="history"  # 🔁 Campo do histórico da conversa
)