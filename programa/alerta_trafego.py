import joblib
import pandas as pd
from prophet import Prophet
from datetime import datetime
from email_module import email, senha, email_destino
import yagmail
import os

LOCAL_ALVO = 'Centro'
LIMITE_ALERTA_CONGESTIONAMENTO = 40   # coloque 1% para testar
PERIODOS_PREVISAO = 15


EMAIL_REMETENTE = email
SENHA_APP = senha
EMAIL_DESTINATARIO = email_destino

def enviar_email(assunto, corpo):

    # --- CORREÇÃO IMPORTANTE ---
    if not EMAIL_REMETENTE or not SENHA_APP:
        print("ERRO: Nenhum email ou senha definidos.")
        return

    try:
        yag = yagmail.SMTP(EMAIL_REMETENTE, SENHA_APP)
        yag.send(to=EMAIL_DESTINATARIO, subject=assunto, contents=corpo)
        print(f"E-mail enviado para {EMAIL_DESTINATARIO}")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

def verificar_alerta():
    try:
        model = joblib.load(f'modelo_prophet_{LOCAL_ALVO}.joblib')
    except:
        print(f"Erro: Modelo 'modelo_prophet_{LOCAL_ALVO}.joblib' não encontrado. Rode o treinamento_prophet.py.")
        return
    
    # Gera previsão
    future = model.make_future_dataframe(periods=PERIODOS_PREVISAO, freq='min', include_history=False)
    forecast = model.predict(future)

    alerta_disparado = False
    detalhes_alerta = []

    print(f"\n--- Monitorando Congestionamento em {LOCAL_ALVO} ---")

    for index, row in forecast.iterrows():
        ds = row['ds']
        yhat = row['yhat']

        if yhat >= LIMITE_ALERTA_CONGESTIONAMENTO:
            detalhes_alerta.append(
                f"⏱ {ds.strftime('%H:%M')} → {yhat:.2f}% (limite {LIMITE_ALERTA_CONGESTIONAMENTO}%)"
            )
            alerta_disparado = True

    if alerta_disparado:
        assunto = f"🚨 ALERTA DE CONGESTIONAMENTO: {LOCAL_ALVO} 🚨"
        corpo = (
            f"O tráfego previsto ultrapassou o limite configurado para {LOCAL_ALVO}.\n\n"
            "⚠ Momentos críticos:\n" +
            "\n".join(detalhes_alerta) +
            f"\n\nLimite definido: {LIMITE_ALERTA_CONGESTIONAMENTO}%"
        )

        print("\n" + assunto)
        print(corpo)
        enviar_email(assunto, corpo)

    else:
        max_yhat = forecast['yhat'].max()
        print(f"✔ Trânsito normal. Pico máximo previsto nos próximos {PERIODOS_PREVISAO} minutos: {max_yhat:.2f}%")

if __name__ == '__main__':
    verificar_alerta()