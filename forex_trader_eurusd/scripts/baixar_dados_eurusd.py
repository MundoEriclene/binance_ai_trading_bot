import requests
import pandas as pd
import os
import time
from dotenv import load_dotenv
from datetime import datetime, timedelta

# ✅ Carregar chave da API do arquivo .env
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../config/.env'))
load_dotenv(dotenv_path)
API_KEY = os.getenv("TWELVE_DATA_API_KEY")

# ⚙️ Configurações
SYMBOL = "EUR/USD"
INTERVAL = "5min"
SAVE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/eurusd_2024_2025.csv'))

START_DATE = datetime(2024, 1, 1)
END_DATE = datetime.now()

# 🔽 Função para baixar um intervalo de dados
def baixar_intervalo(inicio, fim):
    url = (
        f"https://api.twelvedata.com/time_series?"
        f"symbol={SYMBOL}&interval={INTERVAL}"
        f"&start_date={inicio.strftime('%Y-%m-%d')}"
        f"&end_date={fim.strftime('%Y-%m-%d')}"
        f"&apikey={API_KEY}&format=JSON&dp=5"
    )
    print(f"🔄 Baixando de {inicio.date()} até {fim.date()}...")
    response = requests.get(url)
    data = response.json()

    if "values" in data:
        df = pd.DataFrame(data["values"])
        df = df.rename(columns={"datetime": "timestamp"})
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        return df
    else:
        print("⚠️ Erro ao baixar:", data)
        return pd.DataFrame()

# 🔁 Baixar dados em blocos de 7 dias com pausa
atual = START_DATE
todos_dados = pd.DataFrame()

while atual <= END_DATE:
    proximo = atual + timedelta(days=7)
    if proximo > END_DATE:
        proximo = END_DATE

    df_parcial = baixar_intervalo(atual, proximo)
    todos_dados = pd.concat([todos_dados, df_parcial], ignore_index=True)

    atual = proximo + timedelta(days=1)
    if atual > END_DATE:
        break  # Encerra o loop corretamente
    time.sleep(10)

# 💾 Salvar tudo no CSV final
if not todos_dados.empty:
    todos_dados = todos_dados.sort_values("timestamp")
    todos_dados.to_csv(SAVE_PATH, index=False)
    print(f"✅ Arquivo salvo com sucesso em: {SAVE_PATH}")
else:
    print("❌ Nenhum dado foi baixado.")
