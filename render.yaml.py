services:
  - type: web
    name: atendente-virtual
    env: python
    region: oregon
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: python run_local.py
    envVars:
      - key: OPENAI_API_KEY
        sync: false
      - key: TWILIO_ACCOUNT_SID
        sync: false
      - key: TWILIO_AUTH_TOKEN
        sync: false
      - key: REDIS_URL
        sync: false
      - key: URL_BANCO_DADOS
        sync: false
      - key: CHAVE_SECRETA
        sync: false