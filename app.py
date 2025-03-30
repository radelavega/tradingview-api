from flask import Flask, request

app = Flask(__name__)

ultimos_precios = {}

@app.route('/webhook', methods=['POST'])
def recibir_precio():
    datos = request.json
    simbolo = datos['simbolo']
    precio = datos['precio']
    ultimos_precios[simbolo.upper()] = precio
    return {"status": "recibido", "simbolo": simbolo, "precio": precio}

@app.route('/precio/<simbolo>', methods=['GET'])
def obtener_precio(simbolo):
    precio = ultimos_precios.get(simbolo.upper())
    if precio:
        return {"simbolo": simbolo.upper(), "precio": precio}
    else:
        return {"error": "Precio no disponible aún."}, 404

if __name__ == '__main__':
    app.run(port=6000)

import requests

# Brokers permitidos
brokers_validos = ["OANDA", "FXCM", "FOREX", "ALPHAVANTAGE"]

@app.route('/precio_broker/<simbolo>/<broker>', methods=['GET'])
def obtener_precio_broker(simbolo, broker):
    api_key = "TU_API_KEY_AQUI"  # ← Reemplaza con tu API Key real de Alpha Vantage

    simbolo = simbolo.upper()
    broker = broker.upper()

    if broker not in brokers_validos:
        return { "error": f"Broker '{{broker}}' no soportado. Usa uno de: {', '.join(brokers_validos)}" }, 400

    from_currency = simbolo[:3]
    to_currency = simbolo[3:]

    url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={{from_currency}}&to_currency={{to_currency}}&apikey={{api_key}}"

    try:
        response = requests.get(url)
        data = response.json()
        precio = data.get("Realtime Currency Exchange Rate", {}).get("5. Exchange Rate")

        if precio:
            return {
                "simbolo": simbolo,
                "broker": broker,
                "precio": float(precio)
            }
        else:
            return { "error": "Precio no disponible. Verifica el símbolo o la API Key." }, 404
    except Exception as e:
        return { "error": f"Error al obtener el precio: {str(e)}" }, 500