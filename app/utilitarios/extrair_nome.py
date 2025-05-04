# app/utilitarios/extrair_nome.py

def extrair_nome(texto):
    """
    Extrai um nome provável a partir de uma mensagem do tipo:
    - "Com Luiz Fernando"
    - "Sou a Paula, mãe da Júlia"
    - "Me chamo Ana."
    - "Aqui é o Jorge."
    """
    texto = texto.lower().strip()

    # Lista de prefixos que devem ser removidos se iniciam a frase
    prefixos = [
        "com ", "sou ", "aqui e ", "aqui é ", "me chamo ", "meu nome é ",
        "quem fala é ", "quem está falando é ", "fala com ", "é o ", "é a "
    ]

    for prefixo in prefixos:
        if texto.startswith(prefixo):
            texto = texto[len(prefixo):]
            break

    # Remove complementos comuns
    for separador in [",", ".", " e ", " da ", " do ", " com ", " para "]:
        if separador in texto:
            texto = texto.split(separador)[0]

    # Capitaliza o nome corretamente
    nome = " ".join([parte.capitalize() for parte in texto.strip().split() if parte])

    # Retorna apenas se tiver 1 ou 2 palavras (nome e sobrenome simples)
    partes = nome.split()
    if len(partes) > 3:
        nome = " ".join(partes[:2])

    return nome
