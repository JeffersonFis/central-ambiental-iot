from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template

app = Flask(__name__)

dados = {

    "temperatura": 0,
    "pressao": 0,
    "altitude": 0,
    "luminosidade": 0
}

estado_led = False

@app.route('/')

def index():

    return render_template('index.html')

@app.route('/dados', methods=['POST'])

def receber_dados():

    global dados

    dados = request.json

    return 'OK'

@app.route('/api/dados')

def api_dados():

    return jsonify(dados)

@app.route('/toggle_led', methods=['POST'])

def toggle_led():

    global estado_led

    requisicao = request.json

    estado_led = requisicao['estado']

    return jsonify({

        "estado": estado_led
    })

@app.route('/estado_led')

def estado_led_api():

    return jsonify({

        "estado": estado_led
    })

if __name__ == '__main__':

    app.run(
        host='0.0.0.0',
        port=5000
    )
