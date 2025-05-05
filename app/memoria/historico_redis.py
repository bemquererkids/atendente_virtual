# app/memoria/historico_redis.py

import os
from langchain_community.chat_message_histories import RedisChatMessageHistory

def obter_memoria_redis(telefone_usuario: str):
    redis_url = os.getenv("REDIS_URL")  # ex: redis://localhost:6379
    if not redis_url:
        raise ValueError("Variável REDIS_URL não configurada")

    session_id = telefone_usuario.strip().replace("whatsapp:", "").replace("+", "")
    return RedisChatMessageHistory(session_id=session_id, url=redis_url)