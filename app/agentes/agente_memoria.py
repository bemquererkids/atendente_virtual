# ✅ agente_memoria.py — Agente com suporte a Tools e memória de sessão

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain.agents import Tool, initialize_agent

from app.memoria.historico_redis import obter_historico_usuario
from app.tools.especialidade_tool import responder_especialidade

# ⚙️ Configuração do modelo de linguagem
# Usando GPT-4 com baixa temperatura para respostas mais consistentes
llm = ChatOpenAI(model="gpt-4", temperature=0.3)

# 🧰 Lista de ferramentas (Tools) que o agente pode invocar
ferramentas = [
    Tool(
        name="responder_especialidade",
        func=responder_especialidade,
        description=(
            "Use esta ferramenta para responder perguntas sobre especialidades da clínica.\n"
            "Aceita perguntas em texto livre (ex: 'Vocês fazem implante?') ou em formato JSON com campos:\n"
            "{'clinica_id': 'bemquerer', 'especialidade': 'implante'}"
        ),
    )
]

# 🧠 Prompt base com comportamento esperado e histórico da conversa
prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é uma secretária acolhedora e atenciosa de uma clínica odontológica."),
    MessagesPlaceholder(variable_name="history"),  # memória da conversa
    ("human", "{input}")  # última mensagem enviada pelo paciente
])

# 🤖 Criação do agente com memória via Redis
# Usa um agente reativo (zero-shot) com suporte a ferramentas
agente_com_memoria = RunnableWithMessageHistory(
    initialize_agent(
        tools=ferramentas,
        llm=llm,
        agent_type="chat-zero-shot-react-description",
        verbose=True,
        handle_parsing_errors=True
    ),
    # Função que retorna o histórico salvo no Redis com base na sessão (telefone)
    get_session_history=lambda session_id: obter_historico_usuario(session_id),
    
    # Chave da entrada principal (mensagem do paciente)
    input_messages_key="input",
    
    # Chave usada para armazenar o histórico da conversa
    history_messages_key="history",

    # ✅ Correção: especificando explicitamente que o agente também espera o campo 'clinica_id'
    input_keys=["input", "clinica_id"]
)