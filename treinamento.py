import pandas as pd
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
import matplotlib.pyplot as plt
import joblib

LOCAL_ALVO = 'Centro'

try:
    df_prophet = pd.read_csv(f'dados_prophet_{LOCAL_ALVO}.csv')
except FileNotFoundError:
    print(f"Erro: Arquivo 'dados_prophet_{LOCAL_ALVO}.csv' não encontrado. Execute o eda_ml_trafego.py primeiro.")
    exit()

df_prophet['ds'] = pd.to_datetime(df_prophet['ds'])

model = Prophet(
    daily_seasonality=True,
    weekly_seasonality=True,
    yearly_seasonality=False
)

print(f"--- Treinando o modelo Prophet para {LOCAL_ALVO} ---")
model.fit(df_prophet)
print("Treinamento concluído.")

future = model.make_future_dataframe(periods=60, freq='min')

forecast=  model.predict(future)

fig1 = model.plot(forecast)
plt.title(f'Previsão de Congestionamento para {LOCAL_ALVO}')
plt.xlabel('Timestamp')
plt.ylabel('Congestionamento (%)')
plt.savefig('previsao_prophet.png')
print("\nGráfico de previsão 'previsao_prophet.png' salvo.")

fig2 = model.plot_components(forecast)
fig2.savefig('componentes_prophet.png')
print("Gráfico de componentes 'componentes_prophet.png' salvo.")

joblib.dump(model, f'modelo_prophet_{LOCAL_ALVO}.joblib')
print(f"Modelo treinado salvo em 'modelo_prophet_{LOCAL_ALVO}.joblib'.")

print("\n--- Previsões Futuras (Últimas 10) ---")
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(10))