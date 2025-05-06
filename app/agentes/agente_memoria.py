# ✅ Importações dos componentes essenciais do LangChain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain.agents import Tool, initialize_agent

# ✅ Importações locais do projeto
from app.memoria.historico_redis import obter_historico_usuario
from app.tools.especialidade_tool import responder_especialidade

# ⚙️ Configuração do modelo LLM
# Estamos usando o GPT-4 com baixa temperatura para manter consistência nas respostas
llm = ChatOpenAI(model="gpt-4", temperature=0.3)

# 🧰 Definição da lista de ferramentas (Tools) disponíveis para o agente
# Aqui incluímos a função responder_especialidade, que pode ser chamada pelo agente quando detectar intenção
ferramentas = [
    Tool(
        name="responder_especialidade",
        func=responder_especialidade,  # função que será executada
        description=(
            "Use esta ferramenta para responder perguntas sobre especialidades da clínica.\n"
            "Aceita perguntas em texto livre (ex: 'Vocês fazem implante?') ou em formato JSON com campos:\n"
            "{'clinica_id': 'bemquerer', 'especialidade': 'implante'}"
        ),
    )
]

# 🧠 Prompt base que guia o comportamento do agente
# Inclui o histórico da conversa e um tom acolhedor, com input humano ao final
prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é uma secretária acolhedora e atenciosa de uma clínica odontológica."),
    MessagesPlaceholder(variable_name="history"),  # memória da conversa
    ("human", "{input}")  # entrada mais recente do usuário
])

# 🤖 Criação do agente com histórico da conversa usando Redis
# O agente usa o tipo "chat-zero-shot-react-description" e pode invocar ferramentas conforme necessário
agente_com_memoria = RunnableWithMessageHistory(
    initialize_agent(
        tools=ferramentas,           # ferramentas que o agente pode usar
        llm=llm,                     # modelo de linguagem configurado
        agent_type="chat-zero-shot-react-description",
        verbose=True,                # log detalhado no console
        handle_parsing_errors=True  # evita falha total em erros de formatação
    ),
    lambda session_id: obter_historico_usuario(session_id),  # função que recupera histórico no Redis
    input_messages_key="input",       # nome da variável com a mensagem atual
    history_messages_key="history"    # nome da variável com o histórico da conversa
)