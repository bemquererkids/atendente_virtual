# app/config/whatsapp_por_clinica.py

WHATSAPP_POR_CLINICA = {
    "whatsapp:+551144361721": "bemquerer",
    # novos números aqui
}

def identificar_clinica_id(remetente):
    return WHATSAPP_POR_CLINICA.get(remetente, "clinica_padrao")