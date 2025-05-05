import gspread
import pandas as pd
import json
from datetime import datetime
from gspread_dataframe import get_as_dataframe

def gerar_config_json_gsheets(sheet_url, cred_path="credenciais_google.json", clinic_id_alvo=None):
    # Mapeamento de colunas do Forms para nomes técnicos
    mapeamento_clinicas = {
        "Carimbo de data/hora": "timestamp",
        "ID único da clínica\nExemplo: odontodente, odontomax": "clinic_id",
        "Nome da clínica": "nome_clinica",
        "Nome da IA (secretária virtual) \nExemplo: Ana, Clara, Dani": "nome_secretaria",
        "Mensagem de apresentação da IA \nExemplo: “Olá, sou a Ana, secretária da Clínica Bem-Querer. Estou aqui para te acolher.”": "apresentacao",
        "Cargo da IA\nExemplo: secretária, assistente virtual, concierge": "cargo_secretaria",
        "CNPJ da clínica": "cnpj",
        "Endereço completo da clínica": "endereco",
        "Telefone / WhatsApp principal (com DDD)": "whatsapp",
        "E-mail principal da clínica": "email",
        "Site da clínica (URL)": "site",
        "Instagram da clínica (@…)": "instagram",
        "Quais públicos vocês atendem regularmente?": "publicos",
        "Como você quer que a IA se comunique com seus pacientes?": "estilo_comunicacao",
        "Qual o nível de formalidade desejado?": "nivel_formalidade",
        "Quais emoções ou dores os pacientes mais expressam?": "dores_pacientes",
        "Sistema de agenda usado hoje\nExemplo: Clinicorp, Simples Dental, WhatsApp, Google Agenda": "sistema_agenda",
        "Nome e e-mail de quem cuida da parte técnica da clínica": "contato_tecnico"
    }

    mapeamento_especialidades = {
        "Carimbo de data/hora": "timestamp",
        "ID da clínica\nExemplo: bemquerer": "clinic_id",
        "Nome da especialidade\nExemplo: Ortodontia": "especialidade",
        "Profissional responsável\nExemplo: Dra. Amanda": "profissional",
        "Esse profissional é responsável clínico da área?": "responsavel_clinico",
        "Palavras-chave associadas à especialidade\nExemplo: aparelho, alinhador, sorriso torto": "palavras_chave",
        "Mensagem personalizada da IA para essa especialidade\nExemplo: aparelho, alinhador, sorriso torto": "mensagem_personalizada"
    }

    # Autenticando com o Google
    gc = gspread.service_account(filename=cred_path)
    sh = gc.open_by_url(sheet_url)

    aba_clinicas = sh.worksheet("clinicas")
    aba_especialidades = sh.worksheet("especialidades")

    df_clinicas = get_as_dataframe(aba_clinicas, dtype=str, header=1).dropna(how="all")
    df_especialidades = get_as_dataframe(aba_especialidades, dtype=str, header=1).dropna(how="all")

    df_clinicas.rename(columns=mapeamento_clinicas, inplace=True)
    df_especialidades.rename(columns=mapeamento_especialidades, inplace=True)

    if clinic_id_alvo:
        df_clinicas = df_clinicas[df_clinicas["clinic_id"] == clinic_id_alvo]
        df_especialidades = df_especialidades[df_especialidades["clinic_id"] == clinic_id_alvo]

    lista_jsons = {}

    for _, clinica in df_clinicas.iterrows():
        cid = clinica["clinic_id"]
        esp_clinica = df_especialidades[df_especialidades["clinic_id"] == cid]

        especialidades = []
        profissionais = []

        for _, linha in esp_clinica.iterrows():
            especialidade = str(linha.get("especialidade", "")).strip()
            profissional = str(linha.get("profissional", "")).strip()

            especialidades.append(especialidade)

            profissionais.append({
                "especialidade": especialidade,
                "nome": profissional,
                "responsavel_clinico": str(linha.get("responsavel_clinico", "")).strip().lower() == "sim",
                "palavras_chave": [p.strip() for p in str(linha.get("palavras_chave", "")).split(",")],
                "mensagem_personalizada": linha.get("mensagem_personalizada", "").strip()
            })

        json_gerado = {
            "clinica_id": cid,
            "contato": {
                "whatsapp": str(clinica.get("whatsapp", "")).strip(),
                "email": str(clinica.get("email", "")).strip(),
                "instagram": str(clinica.get("instagram", "")).strip(),
                "site": str(clinica.get("site", "")).strip()
            },
            "secretaria_ia": {
                "nome": clinica.get("nome_secretaria", "Assistente"),
                "cargo": clinica.get("cargo_secretaria", "secretária"),
                "apresentacao": clinica.get("apresentacao", "Olá! Sou a assistente da clínica.")
            },
            "especialidades_ativas": especialidades,
            "profissionais": profissionais,
            "atende_criancas": "Crianças" in str(clinica.get("publicos", "")),
            "atende_TEA": "TEA" in str(clinica.get("publicos", "")),
            "data_geracao": datetime.utcnow().isoformat(),
            "versao": "1.0.0"
        }

        lista_jsons[cid] = json_gerado

    return lista_jsons
