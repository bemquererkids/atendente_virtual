import os
import shutil

# Lista de arquivos a remover (relativos à raiz do projeto)
ARQUIVOS_A_REMOVER = [
    "app/agentes/agente_virtual.py",
    "app/utilitarios/chatgpt.py",
    "app/utilitarios/respostas_especialidades.py",
    "app/utilitarios/detectar_intencao.py",
    "app/tools/faq_tool.py",
    "app/tools/especialidade_tool.py",
    "app/tools/lead_tool.py",
    "app/tools/profissionais_tool.py",
    "app/tools/prompt_secretaria_intencao_router.py",
    "app/tools/gpt_tool.py",
    "app/tools/__init__.py",
    "app/utilitarios/contexto_clinica.py"
]

# Lista de pastas a remover (relativas à raiz do projeto)
PASTAS_A_REMOVER = [
    "app/tools",
]

def remover_arquivo(caminho):
    if os.path.exists(caminho):
        os.remove(caminho)
        print(f"✅ Arquivo removido: {caminho}")
    else:
        print(f"⚠️ Arquivo não encontrado: {caminho}")

def remover_pasta(caminho):
    if os.path.exists(caminho):
        shutil.rmtree(caminho)
        print(f"✅ Pasta removida: {caminho}")
    else:
        print(f"⚠️ Pasta não encontrada: {caminho}")

if __name__ == "__main__":
    print("🔎 Iniciando limpeza da estrutura antiga...\n")

    for arquivo in ARQUIVOS_A_REMOVER:
        remover_arquivo(arquivo)

    for pasta in PASTAS_A_REMOVER:
        remover_pasta(pasta)

    print("\n🎉 Limpeza concluída com sucesso.")