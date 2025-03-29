from flask import Flask, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

ALPHA_VANTAGE_API_KEY = "TU_API_KEY_ALPHA_VANTAGE"

# Consulta Precio Forex (Alpha Vantage)
@app.route('/precio_forex', methods=['POST'])
def precio_forex():
    data = request.json
    simbolo = data['simbolo']

    url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={simbolo[:3]}&to_currency={simbolo[3:]}&apikey={ALPHA_VANTAGE_API_KEY}'
    response = requests.get(url).json()

    if "Realtime Currency Exchange Rate" in response:
        rate = response["Realtime Currency Exchange Rate"]
        return {
            "simbolo": simbolo,
            "precio": rate["5. Exchange Rate"],
            "ultima_actualizacion": rate["6. Last Refreshed"]
        }
    else:
        return {"error": "Datos no disponibles"}

# Calendario Económico (Forex Factory)
@app.route('/calendario_economico', methods=['GET'])
def calendario_economico():
    url = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
    calendario = requests.get(url).json()

    eventos_importantes = [
        {"title": e["title"], "date": e["date"], "currency": e["country"], "impact": e["impact"]}
        for e in calendario if e["impact"] == "High"
    ]

    return {"eventos": eventos_importantes}

# Calendario Económico vía Investing.com (scraping)
@app.route('/calendario_investing', methods=['GET'])
def calendario_investing():
    url = "https://es.investing.com/economic-calendar/"
    headers = {"User-Agent": "Mozilla/5.0"}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    eventos = []
    for row in soup.select("table.genTbl tbody tr")[1:10]:
        hora = row.select_one("td.time").text.strip()
        moneda = row.select_one("td.flagCur").text.strip()
        evento = row.select_one("td.event").text.strip()
        impacto = row.get('data-importance', 'N/A')

        eventos.append({"hora": hora, "moneda": moneda, "evento": evento, "impacto": impacto})

    return {"eventos": eventos}

# COT Reports (CFTC)
@app.route('/cot_reports', methods=['GET'])
def cot_reports():
    url = "https://www.cftc.gov/dea/newcot/f_disagg.txt"
    response = requests.get(url)

    data_lines = response.text.splitlines()
    latest_data = data_lines[0:5]  # últimas 5 líneas como ejemplo simplificado

    return {"cot_data_sample": latest_data}

if __name__ == '__main__':
    app.run(port=5001)
