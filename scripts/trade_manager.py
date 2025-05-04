from binance.client import Client
import os
from config.config import BINANCE_API_KEY, BINANCE_API_SECRET

# Inicializando a API Binance
binance_client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

# Função para pegar dados históricos do BTC/USD
def get_historical_data(symbol="BTCUSDT", interval="1h", start_time="1 Jan, 2024", end_time="1 Apr, 2025"):
    candles = binance_client.get_historical_klines(symbol, interval, start_time, end_time)
    return candles

# Função para registrar uma operação
def record_trade(symbol, action, entry_price, exit_price, lot_size, stop_loss, take_profit, balance):
    print(f"Trade {action} | {symbol} | Entrada: {entry_price} | TP: {take_profit} | SL: {stop_loss} | Saldo: {balance} USD")

    # Aqui você pode adicionar um sistema de registro em arquivo ou banco de dados para salvar essas informações.
