import os
import json
from app.utilitarios.gerar_config_json_gsheets import gerar_config_json_gsheets
import pandas as pd
import gspread

# Configurações
SHEET_URL = "https://docs.google.com/spreadsheets/d/1H9scdE_D8YczenSd3DUaz542OdX5uTcH5cIpTwCWgx4/edit?resourcekey=&gid=494481219#gid=494481219"
CRED_PATH = "credenciais_google.json"
PASTA_CONFIGS = "configs"

# Acesso à planilha
gc = gspread.service_account(filename=CRED_PATH)
spreadsheet = gc.open_by_url(SHEET_URL)
aba_clinicas = spreadsheet.worksheet("clinicas")

# Leitura da aba de clínicas como DataFrame
dados_clinicas = aba_clinicas.get_all_records()
df_clinicas = pd.DataFrame(dados_clinicas)

# Verifica se tem a coluna "ID único da clínica"
coluna_id = "ID único da clínica\nExemplo: odontodente, odontomax"
if coluna_id not in df_clinicas.columns:
    raise ValueError(f"❌ Coluna '{coluna_id}' não encontrada na aba 'clinicas'. Verifique o nome exato.")

# Criação da pasta configs
os.makedirs(PASTA_CONFIGS, exist_ok=True)

# Para cada clínica, gera JSON
for _, row in df_clinicas.iterrows():
    clinic_id = row[coluna_id]
    if not clinic_id:
        continue
    print(f"🔄 Gerando JSON para clínica: {clinic_id}")
    config = gerar_config_json_gsheets(SHEET_URL, CRED_PATH, clinic_id_alvo=clinic_id)
    path_arquivo = os.path.join(PASTA_CONFIGS, f"{clinic_id}.json")
    with open(path_arquivo, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print(f"✅ JSON salvo em {path_arquivo}")

print("🎉 Todos os JSONs foram gerados com sucesso!")