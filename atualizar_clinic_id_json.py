import os
import json
import gspread
import pandas as pd

# Configurações
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1H9scdE_D8YczenSd3DUaz542OdX5uTcH5cIpTwCWgx4/edit"
CAMINHO_CRED = "credenciais_google.json"
CAMINHO_ARQUIVO_JSON = "configs/clinic_id.json"

# Conecta com o Google Sheets
gc = gspread.service_account(filename=CAMINHO_CRED)
planilha = gc.open_by_url(URL_PLANILHA)

# Corrige: seleciona a aba correta
aba = planilha.worksheet("clinicas")

# Lê os dados ignorando a primeira linha (que parece conter outra coisa)
dados = aba.get_all_values()[1:]
cabecalho = dados[0]
linhas = dados[1:]

# Cria DataFrame
df = pd.DataFrame(linhas, columns=cabecalho)

# Valida colunas necessárias
if "whatsapp" not in df.columns or "clinic_id" not in df.columns:
    raise ValueError("⚠️ A planilha precisa conter as colunas 'whatsapp' e 'clinic_id'.")

# Cria dicionário com número limpo => clinic_id
def limpar_numero(numero):
    return "".join([c for c in numero if c.isdigit()])

mapeamento = {
    limpar_numero(row["whatsapp"]): row["clinic_id"]
    for _, row in df.iterrows()
    if row["whatsapp"] and row["clinic_id"]
}

# Cria pasta configs se não existir
os.makedirs("configs", exist_ok=True)

# Salva em JSON
with open(CAMINHO_ARQUIVO_JSON, "w", encoding="utf-8") as f:
    json.dump(mapeamento, f, indent=2, ensure_ascii=False)

print(f"✅ Arquivo '{CAMINHO_ARQUIVO_JSON}' atualizado com sucesso.")