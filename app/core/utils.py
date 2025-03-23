import os
import pandas as pd
import datetime
from ta.momentum import RSIIndicator
from binance.client import Client

# Carregar dados da Binance (só leitura)
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")
client = Client(API_KEY, API_SECRET)

# === Calcular RSI com candles da Binance ===
def calcular_rsi(symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_5MINUTE, window=14):
    try:
        klines = client.get_klines(symbol=symbol, interval=interval, limit=window+1)
        closes = [float(k[4]) for k in klines]  # preço de fechamento
        df = pd.DataFrame(closes, columns=["close"])
        rsi = RSIIndicator(close=df["close"], window=window).rsi().iloc[-1]
        return rsi
    except Exception as e:
        print(f"Erro ao calcular RSI: {e}")
        return None

# === Registrar trade em arquivo log ===
def registrar_trade(tipo, preco, quantidade, lucro=None):
    try:
        agora = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        linha = f"{agora},{tipo},{preco},{quantidade}"
        if lucro is not None:
            linha += f",{lucro}"
        linha += "\n"

        os.makedirs("logs", exist_ok=True)
        with open("logs/trades.log", "a") as f:
            f.write(linha)

    except Exception as e:
        print(f"Erro ao registrar trade: {e}")
