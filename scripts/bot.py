import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
from binance.client import Client

# Defina suas credenciais da Binance
BINANCE_API_KEY = "sua_api_key"
BINANCE_API_SECRET = "seu_api_secret"
client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

# Saldo inicial e configuração de risco
initial_balance = 10000  # Saldo inicial em USD
balance = initial_balance
lot_size = 0.01  # Exemplo: 1% do saldo por operação
leverage = 10  # Alavancagem configurada como exemplo

# Função para obter os dados históricos de candles da Binance
def get_historical_data(symbol="BTCUSDT", interval="1h", limit=500):
    # Usando a API da Binance para pegar dados históricos de 1h do BTC/USDT
    candles = client.get_historical_klines(symbol, interval, limit=limit)
    # Organizando os dados em um DataFrame do pandas
    data = []
    for candle in candles:
        timestamp = pd.to_datetime(candle[0], unit='ms')
        open_price = float(candle[1])
        high = float(candle[2])
        low = float(candle[3])
        close = float(candle[4])
        volume = float(candle[5])
        data.append([timestamp, open_price, high, low, close, volume])
    return data

# Função para calcular o risco da operação (1% do saldo)
def calculate_risk(balance, stop_loss, entry_price, leverage=1):
    risk_per_trade = 0.01 * balance * leverage  # 1% do saldo multiplicado pela alavancagem
    risk = entry_price - stop_loss
    lot_size = risk_per_trade / risk  # Tamanho da posição
    return lot_size

# Função para salvar operações em CSV
def save_trade_to_csv(trade_data):
    with open('trades.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(trade_data)

# Função para salvar estatísticas em TXT
def save_statistics_to_txt(wins, losses, drawdown, daily_loss, max_loss):
    with open('statistics.txt', 'w') as file:
        file.write(f"Taxa de Assertividade: {wins / (wins + losses)}\n")
        file.write(f"Drawdown: {drawdown}%\n")
        file.write(f"Prejuízo Máximo Diário: {daily_loss}\n")
        file.write(f"Prejuízo Máximo Total: {max_loss}\n")

# Função para calcular as médias móveis
def calculate_sma(data, short_window=50, long_window=200):
    data['SMA50'] = data['close'].rolling(window=short_window).mean()
    data['SMA200'] = data['close'].rolling(window=long_window).mean()
    return data

# Função para gerar sinais de compra/venda
def generate_signals(data):
    data['Signal'] = 0
    # Usando .iloc para fatiarem por posição, em vez de .loc
    data.iloc[50:, data.columns.get_loc('Signal')] = np.where(data['SMA50'][50:] > data['SMA200'][50:], 1, 0)
    data['Position'] = data['Signal'].diff()
    return data

# Função principal para rodar o bot
def run_bot():
    global balance
    wins, losses = 0, 0
    max_loss = 0
    max_balance = initial_balance
    min_balance = initial_balance
    daily_loss = 0

    candles = get_historical_data()  # Chama a função para obter os dados históricos
    data = pd.DataFrame(candles, columns=["timestamp", "open", "high", "low", "close", "volume"])
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    data.set_index('timestamp', inplace=True)
    data['close'] = data['close'].astype(float)

    # Calcular as médias móveis e gerar sinais
    data = calculate_sma(data)
    data = generate_signals(data)

    # Lógica de operações de compra e venda
    for i in range(50, len(data)):
        if data['Position'].iloc[i] == 1:  # Compra
            entry_price = data['close'].iloc[i]
            stop_loss = entry_price * 0.98  # SL 2% abaixo do preço de entrada
            take_profit = entry_price * 1.02  # TP 2% acima do preço de entrada
            lot_size = calculate_risk(balance, stop_loss, entry_price, leverage=leverage)

            balance -= lot_size * entry_price  # Subtrai o valor da compra
            save_trade_to_csv([entry_price, take_profit, stop_loss, "Compra", balance, data['timestamp'].iloc[i]])

            # Simula a venda no take profit ou stop loss
            exit_price = take_profit
            balance += lot_size * exit_price  # Aumenta o saldo com a venda
            save_trade_to_csv([entry_price, exit_price, stop_loss, "Venda", balance, data['timestamp'].iloc[i]])

            if balance > initial_balance:
                wins += 1
            else:
                losses += 1

        elif data['Position'].iloc[i] == -1:  # Venda
            entry_price = data['close'].iloc[i]
            stop_loss = entry_price * 1.02  # SL 2% acima do preço de entrada
            take_profit = entry_price * 0.98  # TP 2% abaixo do preço de entrada
            lot_size = calculate_risk(balance, stop_loss, entry_price, leverage=leverage)

            balance += lot_size * entry_price  # Subtrai o valor da venda
            save_trade_to_csv([entry_price, take_profit, stop_loss, "Venda", balance, data['timestamp'].iloc[i]])

            # Simula a compra no take profit ou stop loss
            exit_price = take_profit  # Simulação de saída no TP
            balance -= lot_size * exit_price  # Aumenta o saldo com a compra
            save_trade_to_csv([entry_price, exit_price, stop_loss, "Compra", balance, data['timestamp'].iloc[i]])

            if balance > initial_balance:
                wins += 1
            else:
                losses += 1

        # Calculando Drawdown
        if balance > max_balance:
            max_balance = balance
        if balance < min_balance:
            min_balance = balance

        # Calculando o Prejuízo Máximo Diário
        if balance < initial_balance - 500:  # Exemplo de prejuízo diário
            daily_loss = initial_balance - balance
            print(f"Prejuízo máximo diário de {daily_loss} USD")
            break

    # Calcule o drawdown
    drawdown = (max_balance - min_balance) / max_balance * 100

    # Salve as estatísticas em um arquivo .txt
    save_statistics_to_txt(wins, losses, drawdown, daily_loss=daily_loss, max_loss=max_loss)

    # Plotar gráfico com os sinais de compra e venda
    plt.figure(figsize=(10,6))
    plt.plot(data['close'], label='Preço do BTC/USD')
    plt.plot(data['SMA50'], label='SMA 50', alpha=0.7)
    plt.plot(data['SMA200'], label='SMA 200', alpha=0.7)
    plt.scatter(data[data['Position'] == 1].index, data['SMA50'][data['Position'] == 1], marker='^', color='g', label="Compra")
    plt.scatter(data[data['Position'] == -1].index, data['SMA50'][data['Position'] == -1], marker='v', color='r', label="Venda")
    plt.legend(loc="best")
    plt.show()

# Executar o bot
if __name__ == "__main__":
    run_bot()
