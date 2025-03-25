from flask import Flask, render_template, jsonify, request
import requests
from googletrans import Translator

app = Flask(__name__)

API_PIADAS = "https://v2.jokeapi.dev/joke/"
translator = Translator() 

def traduzir_texto(texto):
    try:
        traducao = translator.translate(texto, src="en", dest="pt")
        return traducao.text
    except Exception as e:
        print("Erro ao traduzir:", e)
        return texto

@app.route("/", methods=["GET"])
def index():
    categoria = request.args.get("categoria", "Any") 
    # Adiciona safe-mode para garantir piadas family-friendly
    url = f"{API_PIADAS}{categoria}?safe-mode"
    resposta = requests.get(url)

    if resposta.status_code == 200:
        dados = resposta.json()

        if dados.get("type") == "twopart":
            piada = dados.get("setup", "Erro ao carregar piada")
            rpiada = dados.get("delivery", "")
        elif dados.get("type") == "single":
            piada = dados.get("joke", "Erro ao carregar piada")
            rpiada = ""
        else:
            piada = "Tipo de piada desconhecido"
            rpiada = ""

        # Traduz se a piada estiver em inglês
        if dados.get("lang", "en") == "en":
            piada = traduzir_texto(piada)
            if rpiada:
                rpiada = traduzir_texto(rpiada)
    else:
        piada = "Erro ao buscar piada"
        rpiada = ""

    return render_template("index.html", piada=piada, rpiada=rpiada, categoria_selecionada=categoria)

@app.route("/nova-piada", methods=["GET"])
def nova_piada():
    categoria = request.args.get("categoria", "Any")
    # Adiciona safe-mode para garantir piadas family-friendly
    url = f"{API_PIADAS}{categoria}?safe-mode"
    resposta = requests.get(url)

    if resposta.status_code == 200:
        dados = resposta.json()

        if dados.get("type") == "twopart":
            piada = dados.get("setup", "Erro ao carregar piada")
            rpiada = dados.get("delivery", "")
        elif dados.get("type") == "single":
            piada = dados.get("joke", "Erro ao carregar piada")
            rpiada = ""
        else:
            piada = "Tipo de piada desconhecido"
            rpiada = ""

        # Traduz se necessário
        if dados.get("lang", "en") == "en":
            piada = traduzir_texto(piada)
            if rpiada:
                rpiada = traduzir_texto(rpiada)
    else:
        piada = "Erro ao buscar piada"
        rpiada = ""

    return jsonify({"piada": piada, "rpiada": rpiada})

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

@app.route("/contato")
def contato():
    return render_template("contato.html")

if __name__ == "__main__":
    app.run(debug=True, port=3000)