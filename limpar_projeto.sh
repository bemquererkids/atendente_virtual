#!/bin/bash
echo "🧹 Limpando arquivos obsoletos..."

# Arquivos da raiz
rm -f popular_especialidades.py
rm -f salvar_json_config.py
rm -f estrutura_projeto.txt
rm -f requisitos.txt
rm -f requirements.txt.save
rm -f remocoes.txt
rm -f leia_me.md
rm -f ajustar_clinica.py
rm -f atualizar_clinic_id.py
rm -f atualizar_clinic_id_json.py
rm -f gerar_todos_jsons.py
rm -f teste_identidade.py
rm -f verificar_identidade.py

# Pasta de prompts antiga
rm -rf prompts_secretaria/

# Tools legadas que foram substituídas
rm -f app/tools/especialidade_tool.py
rm -f app/tools/faq_tool.py
rm -f app/tools/lead_tool.py
rm -f app/tools/profissionais_tool.py
rm -f app/tools/prompt_secretaria_intencao_router.py

# Agente anterior
rm -f app/agentes/agente_virtual.py

# Utilitários que foram substituídos
rm -f app/utilitarios/chatgpt.py
rm -f app/utilitarios/detectar_intencao.py
rm -f app/utilitarios/respostas_especialidades.py
rm -f app/utilitarios/contexto_clinica.py
rm -f app/utilitarios/abordagem_inicial.py
rm -f app/utilitarios/gerar_config_json_gsheets.py
rm -f app/utilitarios/twilio.py

# Arquivos temporários e do macOS
find . -name ".DS_Store" -delete

echo "✅ Limpeza concluída com sucesso!"
