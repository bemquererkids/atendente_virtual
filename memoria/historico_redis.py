# app/memoria/historico_redis.py

from langchain.memory import ChatMessageHistory
from langchain.memory.chat_message_histories import RedisChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
import os

# Variáveis de ambiente obrigatórias para o Redis funcionar
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
PREFIXO_CHAVE_REDIS = "memoria_conversa:"


def obter_chave_memoria(session_id: str) -> str:
    """
    Gera uma chave padronizada para armazenar o histórico de conversa no Redis.
    """
    return f"{PREFIXO_CHAVE_REDIS}{session_id}"


def criar_memoria_com_redis(session_id: str) -> ChatMessageHistory:
    """
    Cria (ou recupera) o histórico de mensagens no Redis baseado em um ID de sessão.
    """
    return RedisChatMessageHistory(
        url=REDIS_URL,
        session_id=obter_chave_memoria(session_id)
    )


def configurar_runnable_com_memoria(runnable_chain) -> RunnableWithMessageHistory:
    """
    Envolve um agente LangChain em um wrapper que adiciona histórico de conversa com Redis.
    """
    return RunnableWithMessageHistory(
        runnable_chain,
        lambda session_id: criar_memoria_com_redis(session_id),
        input_messages_key="input",
        history_messages_key="chat_history",
    )
