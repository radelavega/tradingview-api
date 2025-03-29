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
