from app.principal import criar_aplicacao

app = criar_aplicacao()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)