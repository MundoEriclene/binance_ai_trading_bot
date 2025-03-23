import os
import pandas as pd
from datetime import datetime
from binance.client import Client
from dotenv import load_dotenv

# Carregar .env
load_dotenv(dotenv_path='../config/.env')

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

# Inicializar cliente da Binance
client = Client(API_KEY, API_SECRET)

# Par e intervalo
symbol = "BTCUSDT"
interval = Client.KLINE_INTERVAL_5MINUTE

# Data de início
start_str = "1 Jan, 2024"

print("⏳ Baixando dados do BTC/USDT em M5 desde 2024...")

# Baixar dados históricos
klines = client.get_historical_klines(symbol, interval, start_str)

# Organizar os dados
df = pd.DataFrame(klines, columns=[
    "timestamp", "open", "high", "low", "close", "volume",
    "close_time", "quote_asset_volume", "number_of_trades",
    "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
])

df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
df.set_index("timestamp", inplace=True)

# Salvar como CSV
output_path = "../data/processed/btc_usdt_m5.csv"
df.to_csv(output_path)

print(f"✅ Dados salvos com sucesso em: {output_path}")
