import requests
import time as tempo
import pandas as pd
from datetime import datetime
from api import API

LOCAIS = [
    {"nome": "Centro", "lat": -23.5505, "lon": -46.6333},
    {"nome": "Avenida Paulista", "lat": -23.561414, "lon": -46.655881},
    {"nome": "Marginal Tiete", "lat": -23.5163, "lon": -46.7375},
    {"nome": "Marginal Pinheiros", "lat": -23.6101, "lon": -46.6977}
]

def coleta_trafego(lat, lon):
    url = f'https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?point={lat},{lon}&key={API}'
    response = requests.get(url)
    data = response.json()

    if "flowSegmentData" not in data:
        print(f"⚠ Erro na API para {lat}, {lon} — resposta:", data)
        return None

    velocidade_atual = data['flowSegmentData']['currentSpeed']
    velocidade_livre = data['flowSegmentData']['freeFlowSpeed']
    congestao = round((1 - (velocidade_atual / velocidade_livre)) * 100, 2)

    return {
        'timestamp': datetime.now(),
        'velocidade_atual': velocidade_atual,
        'velocidade_livre': velocidade_livre,
        'congestao': congestao
    }

def save_data(dados):
    try:
        df = pd.read_csv('dados_trafego_sp.csv')
        df = pd.concat([df, pd.DataFrame([dados])], ignore_index=True)
    except:
        df = pd.DataFrame([dados])

    df.to_csv("dados_trafego_sp.csv", index=False)
    print("💾 Dados Salvos:", dados)

if __name__ == '__main__':
    while True:
        print("\n🔎 Iniciando nova coleta...\n")

        for local in LOCAIS:
            resultado = coleta_trafego(local["lat"], local["lon"])

            if resultado is None:
                continue

            dados = {
                "timestamp": resultado["timestamp"],
                "local": local["nome"],
                "lat": local["lat"],
                "lon": local["lon"],
                "velocidade_atual": resultado["velocidade_atual"],
                "velocidade_livre": resultado["velocidade_livre"],
                "congestao": resultado["congestao"]
            }

            save_data(dados)

        print("\n⏳ Aguardando 3 minutos para próxima coleta...\n")
        tempo.sleep(190)
