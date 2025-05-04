# app/utilitarios/chatgpt.py

import openai
import os
from app.config.identidade_secretaria import IDENTIDADE, CONTEXTO_CLINICA, INSTRUCOES_ATENDIMENTO

openai.api_key = os.getenv("OPENAI_API_KEY")

def gerar_resposta_informativa(mensagem: str, nome: str = "") -> str:
    try:
        prompt = f'''
Você é {IDENTIDADE['NOME_SECRETARIA']}, {IDENTIDADE['PERSONA_SECRETARIA']}, que atua na clínica {IDENTIDADE['NOME_CLINICA']}.

{CONTEXTO_CLINICA}

Mensagem do paciente: "{mensagem}"

{INSTRUCOES_ATENDIMENTO}

Responda de forma acolhedora, clara e objetiva, com no máximo 5 linhas.
Se souber o nome do paciente, use-o na resposta (ex: "{nome}").
'''

        resposta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é uma secretária humana, acolhedora, inteligente e da área odontológica."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=300,
            n=1,
        )

        return {"content": resposta.choices[0].message["content"].strip()}

    except Exception as e:
        print(f"[ERRO] ao gerar resposta GPT: {e}")
        return "Desculpe, estou com uma instabilidade no momento. Pode tentar novamente? 🌻"