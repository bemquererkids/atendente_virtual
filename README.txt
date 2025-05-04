# Secretária Virtual (Projeto Genérico para Clínicas)

Este projeto é uma solução de secretária virtual personalizável e humanizada, construída para ser utilizada por diferentes clínicas odontológicas (ou médicas) com identidades únicas.

O nome da secretária, estilo de comunicação, equipe de profissionais, serviços oferecidos e dados de contato são todos parametrizados através de um arquivo de configuração `.json` gerado dinamicamente a partir de um Google Form padronizado.

---

## 📁 Estrutura do Projeto

```
atendente_virtual/
├── app/
│   ├── agentes/                    # Agente LangChain
│   ├── config/
│   │   └── identidade_clinica.py  # Carrega a configuração dinâmica
│   ├── tools/
│   │   ├── prompt_loader.py
│   │   └── prompt_secretaria_intencao_router.py
│   ├── utilitarios/
│   │   └── contexto_clinica.py    # Função carregar_config_clinica
│   └── ...
├── configs/
│   └── bemquerer.json             # Exemplo de configuração para a Bem-Querer
├── prompts_secretaria/
│   ├── prompt_secretaria_identidade.md
│   ├── prompt_secretaria_fluxo_conducao.md
│   └── intencao_respostas_secretaria.json
├── executar.py                    # Entry point para renderização
```

---

## 🧩 Funcionamento

### 1. **Formulário Google → JSON da Clínica**
Um script Apps Script lê automaticamente a última resposta do formulário e gera um arquivo `.json` com:

- Nome da clínica, contatos, especialidades
- Lista de profissionais (nome, CRO, especialidade, duração)
- Nome da secretária IA, estilo de apresentação
- Indicação se atende TEA, crianças, etc.
- Campo `clinica_id`, `versao`, `data_geracao`

O arquivo é salvo automaticamente no Google Drive na pasta:
```
Config_<clinica_id>/
└── <clinica_id>_config_<timestamp>.json
```

### 2. **Carregamento da Configuração no Python**
O arquivo `app/utilitarios/contexto_clinica.py` possui:
```python
carregar_config_clinica(clinica_id="bemquerer")
```
O conteúdo é carregado para `config_clinica`, e fica disponível para os fluxos, ferramentas e prompts.

### 3. **Uso nos fluxos e geração de mensagens**
- Os prompts são carregados de `prompts_secretaria/`
- O nome da secretária, apresentação e profissionais são inseridos dinamicamente nos fluxos de conversa, geração de mensagens e agendamentos.
- O roteamento inteligente baseado em intenção está em `prompt_secretaria_intencao_router.py`

---

## 🔁 Para adaptar a nova clínica
1. Envie o formulário (ou duplique)
2. Gere o JSON no Drive (automaticamente com timestamp)
3. Baixe ou sincronize para a pasta `configs/`
4. Altere em `identidade_clinica.py` o `CLINICA_ID_ATIVA = "nova_clinica"`
5. Pronto! Toda a aplicação usará a nova identidade

---

## 📌 Observações finais

- O nome "Clara" não está presente no código. Ele virá do JSON da clínica.
- O sistema suporta múltiplas clínicas e múltiplas secretárias.
- Pode ser expandido para médicos, psicólogos, veterinários, etc.
- O código não referencia nomes fixos. Tudo é dinâmico com base em `config_clinica`

---

## ✨ Pronto para escalar
Este projeto está estruturado para ser white-label. Cada cliente poderá:
- Ter seu próprio formulário
- Gerar sua configuração personalizada
- Personalizar os fluxos e a IA com seu tom de voz
- Usar uma instância única da plataforma sem acoplar nomes ou arquivos fixos

---

> Para dúvidas técnicas ou evolução do produto, consulte `app/utilitarios/contexto_clinica.py`, `prompt_loader.py` e `prompt_secretaria_intencao_router.py`.
