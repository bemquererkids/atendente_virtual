# app/memoria/historico_redis.py


from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.chat_message_histories import RedisChatMessageHistory
import os

def obter_historico_usuario(user_id: str) -> ChatMessageHistory:
    """
    Retorna o histórico de mensagens do usuário, persistido no Redis.
    """
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    return RedisChatMessageHistory(session_id=user_id, url=redis_url)



