import os
import json

# Simulando o JSON gerado
config = {
    "clinica_id": "bemquerer",
    "contato": {
        "whatsapp": "(011) 4436-1721",
        "email": "bemquererodontologia@gmail.com",
        "instagram": "https://www.instagram.com/bemquererodontologia/",
        "site": "www.bemquererodontologia.com.br"
    },
    "secretaria_ia": {
        "nome": "Ana",
        "cargo": "secretária",
        "apresentacao": "Olá, sou a Ana, secretária da Clínica Bem-Querer. Estou aqui para te acolher."
    },
    "especialidades_ativas": [
        "TEA"
    ],
    "profissionais": [
        {
            "especialidade": "TEA",
            "nome": "Dra. Vanessa Battistini",
            "responsavel_clinico": True,
            "palavras_chave": [
                "tea", "autismo", "espectro autista", "autista", "paciente autista",
                "criança autista", "pessoa com autismo", "atendimento autismo",
                "atendimento para autista", "atendimento adaptado", "neurodivergente",
                "neurodivergência", "criança especial", "paciente especial",
                "atendimento especial", "pne", "necessidades especiais",
                "paciente com necessidades especiais", "deficiência", "síndrome",
                "síndromes raras", "síndrome de down", "down", "atendimento down",
                "deficiente", "paciente atípico", "criança atípica",
                "desenvolvimento atípico", "atendimento com paciência", "calma",
                "acolhimento", "inclusão", "paciente sensível", "hipersensível",
                "sensibilidade", "adaptação", "ambiente calmo", "ambiente adaptado",
                "ambiente lúdico", "acolhimento especial", "resistência ao dentista",
                "medo do dentista", "criança com medo", "criança não colabora",
                "dificuldade de atendimento", "consultório adaptado",
                "dentista para autista", "dentista para crianças com TEA",
                "dentista especial", "dentista humanizado", "dentista TEA",
                "dentista PNE", "sedação", "sedação endovenosa", "sedação para autista",
                "sedar", "criança agitada", "comportamento difícil",
                "comportamento resistente", "consulta difícil", "consultório sensorial",
                "sala sensorial", "luz baixa", "som baixo", "cheiro neutro"
            ],
            "mensagem_personalizada": (
                "Aqui na nossa clínica, o atendimento a pacientes com TEA, síndromes raras ou necessidades especiais "
                "é feito com muito acolhimento, paciência e respeito às particularidades de cada um.\n"
                "Nossa equipe é preparada para oferecer um ambiente adaptado, calmo e sensorialmente seguro, com "
                "tempo estendido e abordagem lúdica quando necessário.\n"
                "Se você estiver buscando um cuidado gentil, com escuta ativa e empatia verdadeira, pode contar conosco. 💙\n"
                "Vamos conversar para entender qual a melhor forma de acolher você (ou seu filho)?"
            )
        }
    ],
    "atende_criancas": True,
    "atende_TEA": True,
    "data_geracao": "2025-05-04T13:06:48.384322",
    "versao": "1.0.0"
}

# Caminho da pasta onde salvar o JSON
pasta_destino = "configs"
os.makedirs(pasta_destino, exist_ok=True)

# Nome do arquivo
nome_arquivo = f"{config['clinica_id']}.json"
caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)

# Salvar o JSON
with open(caminho_arquivo, "w", encoding="utf-8") as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

print(f"✅ Configuração salva em: {caminho_arquivo}")