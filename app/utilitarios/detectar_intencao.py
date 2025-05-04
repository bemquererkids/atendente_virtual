def detectar_intencao_basica(texto: str) -> str:
    texto = texto.lower().strip()
    if not texto:
        return ""

    # 1. Atendimento Especial (TEA, PNE, síndromes)
    termos_tea_pne = [
        "autista", "tea", "transtorno do espectro", "síndrome", "síndrome de down",
        "neurodivergente", "pne", "necessidades especiais", "paciente especial",
        "tdah", "asperger", "criança especial", "atípico", "sensorial"
    ]
    if any(t in texto for t in termos_tea_pne):
        return "atendimento_especial"

    # 2. Odontopediatria
    termos_odontopediatria = [
        "odontopediatria", "pediatria", "dentista infantil", "dentista criança",
        "primeira consulta", "dente de leite", "freio lingual", "freio labial", "frenectomia",
        "língua presa", "fala presa", "amamentação", "mamilo invertido", "não mama", "desmame"
    ]
    if any(t in texto for t in termos_odontopediatria):
        return "odontopediatria"

    # 3. Ortodontia
    termos_ortodontia = [
        "ortodontia", "aparelho", "dentes tortos", "corrigir mordida", "apinhamento",
        "aparelho fixo", "mordida cruzada", "mordida aberta", "diastema", "encaixe errado"
    ]
    if any(t in texto for t in termos_ortodontia):
        return "ortodontia"

    # 4. Invisalign (Alinhadores)
    termos_invisalign = [
        "invisalign", "alinhador", "aparelho invisível", "alinhadores invisíveis",
        "placa invisível", "alinhador transparente"
    ]
    if any(t in texto for t in termos_invisalign):
        return "invisalign"

    # 5. Implantes
    termos_implantes = [
        "implante", "implantes", "falta dente", "perdi dente", "repor dente",
        "parafuso", "colocar dente", "dente com pino"
    ]
    if any(t in texto for t in termos_implantes):
        return "implante"

    # 6. Próteses
    termos_proteses = [
        "prótese", "protese", "ponte móvel", "dentadura", "prótese total", "encaixe dente",
        "prótese protocolo", "coroa provisória"
    ]
    if any(t in texto for t in termos_proteses):
        return "protese"

    # 7. Sedação
    termos_sedacao = [
        "sedação", "sedacao", "anestesia", "tenho medo", "ansioso", "tranquilizar",
        "dormir para tratar", "medo de dentista", "oxido nitroso", "endovenosa", "sedado"
    ]
    if any(t in texto for t in termos_sedacao):
        return "sedacao"

    # 8. Estética
    termos_estetica = [
        "clareamento", "lentes de contato", "lente", "sorriso bonito", "estética",
        "dente branco", "embelezar", "harmonização", "resina estética"
    ]
    if any(t in texto for t in termos_estetica):
        return "estetica"

    # 9. Periodontia
    termos_periodontia = [
        "gengiva", "periodontia", "gengivite", "sangramento gengival", "gengiva inflamada",
        "tártaro avançado", "bolsa periodontal", "tratamento periodontal", "limpeza profunda"
    ]
    if any(t in texto for t in termos_periodontia):
        return "periodontia"

    # 10. Endodontia (Canal)
    termos_endodontia = [
        "canal", "endodontia", "tratamento de canal", "nervo exposto", "dente escurecido",
        "infecção interna", "dor profunda", "pulpite", "necrose dentária"
    ]
    if any(t in texto for t in termos_endodontia):
        return "endodontia"

    # 11. Dentística Restauradora
    termos_dentistica = [
        "restauração", "restaurar", "dente quebrado", "obturação", "cárie", "carie",
        "resina", "fechar buraco", "fratura dental", "trincado"
    ]
    if any(t in texto for t in termos_dentistica):
        return "dentistica"

    # 12. DTM / ATM
    termos_dtm = [
        "dtm", "atm", "dor ao mastigar", "estalo na mandíbula", "problema na articulação",
        "dor na face", "desvio mandibular", "tensão no maxilar"
    ]
    if any(t in texto for t in termos_dtm):
        return "dtm"

    # 13. Cirurgia Bucomaxilofacial
    termos_bucomaxilo = [
        "bucomaxilo", "buco maxilo", "cirurgia ortognática", "extração complicada",
        "dente incluso", "cisto ósseo", "lesão óssea", "biopsia", "terceiro molar"
    ]
    if any(t in texto for t in termos_bucomaxilo):
        return "bucomaxilo"

    # 14. Dor / Emergência
    termos_dor = [
        "dor", "urgência", "emergência", "dente inflamado", "dente latejando", "abscesso",
        "quebrou o dente", "inchado", "dor forte", "incomodando muito"
    ]
    if any(t in texto for t in termos_dor):
        return "dor"

    # 15. Consulta de rotina
    termos_rotina = [
        "check-up", "limpeza", "manutenção", "preventivo", "higienização", "avaliação",
        "consulta periódica", "revisão"
    ]
    if any(t in texto for t in termos_rotina):
        return "consulta_rotina"

    # 16. Preço / Convênio
    termos_preco = [
        "preço", "valor", "quanto custa", "investimento", "parcelamento",
        "aceita convênio", "plano dental", "aceita plano"
    ]
    if any(t in texto for t in termos_preco):
        return "preco"

    # 17. Retorno
    termos_retorno = [
        "retorno", "reconsulta", "voltar", "acompanhamento", "nova etapa", "continuar tratamento"
    ]
    if any(t in texto for t in termos_retorno):
        return "retorno"

    # 18. Interesse geral
    termos_geral = [
        "tratamento", "especialidade", "vocês fazem", "procedimento", "serviço", "oferecem"
    ]
    if any(t in texto for t in termos_geral):
        return "especialidade"

    # 19. FAQ
    termos_faq = [
        "telefone", "whatsapp", "endereço", "como chegar", "localização", "mapa",
        "estacionamento", "funciona", "horário", "abrem", "dias disponíveis"
    ]
    if any(t in texto for t in termos_faq):
        return "faq"

    return ""

    return ""

# Alias para manter compatibilidade com nome antigo
detectar_intencao_mensagem = detectar_intencao_basica