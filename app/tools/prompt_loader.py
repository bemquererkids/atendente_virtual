import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
PROMPTS_DIR = os.path.abspath(os.path.join(BASE_PATH, '../../prompts_secretaria'))

def carregar_prompt(nome_arquivo):
    caminho = os.path.join(PROMPTS_DIR, nome_arquivo)
    with open(caminho, 'r', encoding='utf-8') as f:
        return f.read()

def carregar_prompts_padrao():
    return {
        "identidade": carregar_prompt("prompt_secretaria_identidade.md"),
        "fluxo_conducao": carregar_prompt("prompt_secretaria_fluxo_conducao.md"),
        "intencao_respostas": os.path.join(PROMPTS_DIR, "intencao_respostas_secretaria.json"),
        "agendamento_especial": carregar_prompt("prompt_agendamento_especial.md")
    }
