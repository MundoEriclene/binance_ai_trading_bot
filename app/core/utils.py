import os
import pandas as pd
import datetime
from ta.momentum import RSIIndicator
from core.binance_api import client  # Reutiliza a conexão centralizada

# === Calcular RSI com candles da Binance ===
def calcular_rsi(symbol="BTCUSDT", interval="5m", window=14):
    try:
        klines = client.get_klines(symbol=symbol, interval=interval, limit=window+1)
        closes = [float(k[4]) for k in klines]
        df = pd.DataFrame(closes, columns=["close"])
        rsi = RSIIndicator(close=df["close"], window=window).rsi().iloc[-1]
        return rsi
    except Exception as e:
        print(f"Erro ao calcular RSI: {e}")
        return None

# === Registrar trade em log ===
def registrar_trade(tipo, preco, quantidade, lucro=None):
    try:
        agora = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        linha = f"{agora},{tipo},{preco},{quantidade}"
        if lucro is not None:
            linha += f",{lucro}"
        linha += "\n"

        os.makedirs("core/logs", exist_ok=True)
        with open("core/logs/trades.log", "a") as f:
            f.write(linha)

    except Exception as e:
        print(f"Erro ao registrar trade: {e}")
