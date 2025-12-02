import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from prophet import Prophet

try:
    df = pd.read_csv('dados_trafego_tratados.csv')
except FileExistsError:
    print('Erro: arquivo "dados_trafego_tratados.csv" não encontrado. Verifique.')
    exit()

print(" --- Análise Exploratória de Dados (EDA) --- ")
print(f'Formato dos dados: {df.shape}')
print("\nPrimeiras 5 linhas:")
print(df.head())
print("\nInformações sobre as colunas:")
print(df.info())
print("\nEstatísticas Descritivas:")
print(df.describe())

LOCAL_ALVO = 'Centro'
COLUNA_ALVO = 'congestao'

df_prophet = df[df['local'] == LOCAL_ALVO].copy()

df_prophet = df_prophet.rename(columns={'timestamp': 'ds', COLUNA_ALVO: 'y'})


df_prophet['ds'] = pd.to_datetime(df_prophet['ds'])
df_prophet['y'] = pd.to_numeric(df_prophet['y'])

df_prophet = df_prophet.drop_duplicates(subset=['ds']).sort_values(by='ds')

print(f"\n--- Preparação para Prophet ({LOCAL_ALVO} - {COLUNA_ALVO}) ---")
print(f"Formato dos dados para Prophet: {df_prophet.shape}")
print(df_prophet[['ds', 'y']].head())

plt.figure(figsize=(12, 6))
sns.lineplot(x='ds', y='y', data=df_prophet)
plt.title(f'Série Temporal de {COLUNA_ALVO} em {LOCAL_ALVO}')
plt.xlabel('Timestamp')
plt.ylabel(COLUNA_ALVO)
plt.savefig('serie_temporal_congestao.png')
print("\nGráfico 'serie_temporal_congestao.png' salvo.")

df_prophet[['ds', 'y']].to_csv(f'dados_prophet_{LOCAL_ALVO}.csv', index=False)
print(f"Dataset preparado para ML salvo em 'dados_prophet_{LOCAL_ALVO}.csv'.")