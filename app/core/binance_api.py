import os
from binance.client import Client
from binance.exceptions import BinanceAPIException

# Carrega as variáveis do .env
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

if not API_KEY or not API_SECRET:
    raise ValueError("⚠️ API_KEY ou API_SECRET não encontrados. Verifique seu .env ou variáveis do Render.")

client = Client(API_KEY, API_SECRET)

# === Função para pegar o preço ao vivo ===
def get_price(symbol="BTCUSDT"):
    try:
        ticker = client.get_symbol_ticker(symbol=symbol)
        return float(ticker['price'])
    except Exception as e:
        print(f"Erro ao obter preço do ativo {symbol}: {e}")
        return None

# === Função para executar compra ===
def buy_crypto(symbol, quantity):
    try:
        order = client.order_market_buy(
            symbol=symbol,
            quantity=round(quantity, 6)
        )
        print(f"🟢 Ordem de COMPRA executada: {order}")
    except BinanceAPIException as e:
        print(f"❌ Erro na compra: {e.message}")
    except Exception as e:
        print(f"❌ Erro inesperado na compra: {e}")

# === Função para executar venda ===
def sell_crypto(symbol, quantity):
    try:
        order = client.order_market_sell(
            symbol=symbol,
            quantity=round(quantity, 6)
        )
        print(f"🔴 Ordem de VENDA executada: {order}")
    except BinanceAPIException as e:
        print(f"❌ Erro na venda: {e.message}")
    except Exception as e:
        print(f"❌ Erro inesperado na venda: {e}")
