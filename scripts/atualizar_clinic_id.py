import os
import json
import gspread

# Caminhos
CRED_PATH = "credenciais_google.json"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1H9scdE_D8YczenSd3DUaz542OdX5uTcH5cIpTwCWgx4/edit"
PATH_JSON = os.path.join("configs", "clinic_id.json")

# Acesso ao Google Sheets
gc = gspread.service_account(filename=CRED_PATH)
planilha = gc.open_by_url(SHEET_URL)
aba = planilha.worksheet("clinic_id")

# Leitura da tabela, ignorando a primeira linha se for de instrução
valores = aba.get_all_values()
cabecalho = valores[1]  # Segunda linha é o cabeçalho verdadeiro
dados = valores[2:]     # Dados a partir da terceira linha

# Índices
idx_telefone = cabecalho.index("telefone_whatsapp")
idx_id_clinica = cabecalho.index("ID único da clínica")

# Monta o dicionário
mapeamento = {}
for linha in dados:
    if len(linha) <= max(idx_telefone, idx_id_clinica):
        continue
    telefone = linha[idx_telefone].strip()
    clinic_id = linha[idx_id_clinica].strip()
    if telefone and clinic_id:
        telefone_limpo = (
            telefone.replace("+", "")
                    .replace("-", "")
                    .replace("(", "")
                    .replace(")", "")
                    .replace(" ", "")
        )
        mapeamento[telefone_limpo] = clinic_id

# Salva o JSON
os.makedirs("configs", exist_ok=True)
with open(PATH_JSON, "w", encoding="utf-8") as f:
    json.dump(mapeamento, f, indent=2, ensure_ascii=False)

print(f"✅ Arquivo 'clinic_id.json' atualizado com sucesso.")