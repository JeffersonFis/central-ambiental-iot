from flask import Flask, request, render_template, jsonify, send_file
import time
import csv
import os

app = Flask(__name__)

dados = {
    "temperatura": 0,
    "umidade": 0,
    "pressao": 0,
    "altitude": 0,
    "luminosidade": 0,
    "online": False,
    "led": False
}

ultimo_recebimento = 0

estado_led = False

arquivo_csv = "medicoes.csv"

if not os.path.exists(arquivo_csv):

    with open(arquivo_csv, mode='w', newline='') as arquivo:

        escritor = csv.writer(arquivo)

        escritor.writerow([
            "Hora",
            "Temperatura",
            "Umidade",
            "Pressao",
            "Altitude",
            "Luminosidade"
        ])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dados', methods=['POST'])
def receber_dados():

    global dados
    global ultimo_recebimento

    dados = request.json

    dados["online"] = True

    dados["led"] = estado_led

    ultimo_recebimento = time.time()

    hora = time.strftime("%H:%M:%S")

    with open(arquivo_csv, mode='a', newline='') as arquivo:

        escritor = csv.writer(arquivo)

        escritor.writerow([
            hora,
            dados["temperatura"],
            dados["umidade"],
            dados["pressao"],
            dados["altitude"],
            dados["luminosidade"]
        ])

    return "OK"

@app.route('/ler_dados')
def ler_dados():

    global dados
    global ultimo_recebimento

    tempo_atual = time.time()

    if tempo_atual - ultimo_recebimento > 3:

        dados = {
            "temperatura": 0,
            "umidade": 0,
            "pressao": 0,
            "altitude": 0,
            "luminosidade": 0,
            "online": False,
            "led": False
        }

    return jsonify(dados)

@app.route('/ligar_led')
def ligar_led():

    global estado_led

    estado_led = True

    return "LED LIGADO"

@app.route('/desligar_led')
def desligar_led():

    global estado_led

    estado_led = False

    return "LED DESLIGADO"

@app.route('/estado_led')
def estado_led_api():

    return jsonify({
        "led": estado_led
    })

@app.route('/baixar_csv')
def baixar_csv():

    return send_file(
        arquivo_csv,
        as_attachment=True
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)