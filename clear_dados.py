import pandas as pd

def clear_dataset(caminho_csv='dados_trafego_sp.csv'):
    df = pd.read_csv(caminho_csv)

    df['timestamp'] = pd.to_datetime(df['timestamp'])

    df['hora'] = df['timestamp'].dt.hour
    df['dia_semana'] = df['timestamp'].dt.weekday
    df['minuto'] = df['timestamp'].dt.minute

    def map_periodo(h):
        if 6 <= h < 12: return 'manha'
        elif 12 <= h < 18: return 'tarde'
        elif 18 <= h <= 23: return 'noite'
        else: return 'madrugada'

    df['periodo'] = df['hora'].apply(map_periodo)

    df = df.drop_duplicates()

    df.to_csv('dados_trafego_tratados.csv', index=False)

    print('Arquivo dados_trafego_tratados.csv gerado com sucesso!')
    print(df.tail())

    return df


if __name__ == "__main__":
    clear_dataset()
