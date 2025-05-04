prompts_secretaria/ — Organização dos Prompts da Secretária Virtual

Este diretório contém os arquivos de prompt que definem o comportamento, tom de voz e lógica da secretária virtual utilizada em diferentes clínicas.

O nome da secretária, sua forma de se apresentar e a estrutura das mensagens variam dinamicamente com base no JSON de configuração da clínica ativa (config_clinica).

📁 Estrutura e Finalidade

prompt_secretaria_identidade.md

Contém o texto-base que define quem é a secretária, como ela se comunica, e quais valores transmite. Exemplo:

Você é {{NOME_SECRETARIA}}, secretária da clínica {{NOME_CLINICA}}. Sua linguagem é empática, objetiva e acolhedora...

Este prompt pode ser usado em qualquer parte da conversa para relembrar ao modelo o tom desejado.

prompt_secretaria_fluxo_conducao.md

Fluxo-base de atendimento organizado em etapas:

Acolhida inicial

Coleta de informações (nome, se é o paciente ou responsável, tipo de atendimento)

Encaminhamento para agendamento ou direcionamento

Usado pelo agente principal para definir a condução do atendimento.

intencao_respostas_secretaria.json

Arquivo auxiliar para mapeamento de intenções (detecção via embeddings ou análise de texto) e suas respectivas respostas.

Exemplo:

{
  "consulta_rotina": "Ótimo! Cuidar da saúde bucal é essencial. Que tal agendar sua consulta preventiva?",
  "urgencia_dor": "Sinto muito por isso. Vamos agendar o mais rápido possível? Me diga o local da dor."
}

🧩 Como os prompts são utilizados

São carregados via prompt_loader.py

Inseridos nos fluxos de conversa automaticamente

Adaptados conforme o nome da secretária e da clínica via config_clinica

🔁 Para adicionar novos prompts

Crie um novo arquivo .md ou .json com nome claro (ex: prompt_agendamento_especial.md)

Atualize prompt_loader.py para incluir a nova entrada

Utilize no agente ou nas ferramentas (tools) conforme necessário

Este diretório deve conter apenas conteúdo textual usado para modelar a comunicação da secretária virtual. Ele é independente da clínica: quem dá identidade a tudo é o arquivo JSON carregado em tempo real.