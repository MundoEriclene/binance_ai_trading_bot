import os
import time
import pandas as pd
from binance.client import Client
from dotenv import load_dotenv
from datetime import datetime

# === CONFIG ===
load_dotenv('/Users/programacao/Documents/binance_ai_trading_bot/config/.env')
api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_API_SECRET')

client = Client(api_key, api_secret)

symbol = "BTCUSDT"
interval = Client.KLINE_INTERVAL_5MINUTE
start_str = "1 Jan, 2023"
end_str = datetime.now().strftime("%d %b, %Y")
saida_csv = "../data/processed/btc_usdt_m5_2023_2025.csv"

print(f"⏳ Baixando dados de {symbol} M5 de {start_str} até {end_str}...")

klines = client.get_historical_klines(symbol, interval, start_str, end_str)
time.sleep(1)

# === TRANSFORMAR EM DATAFRAME ===
df = pd.DataFrame(klines, columns=[
    "timestamp", "open", "high", "low", "close", "volume",
    "close_time", "quote_asset_volume", "number_of_trades",
    "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
])

df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')
df.to_csv(saida_csv, index=False)

print(f"✅ Dados salvos em: {saida_csv}")
