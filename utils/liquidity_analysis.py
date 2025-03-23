import os
import sqlite3
import pandas as pd
import json
import time
import logging

# 🔥 Configurar Logs
log_dir = "logs"
log_file = f"{log_dir}/liquidity.log"

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(level=logging.INFO, filename=log_file, filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s")

# 🔄 Função para analisar a liquidez do Order Book
def analisar_liquidez():
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect("data/trading_data.db")
        cursor = conn.cursor()

        # Buscar os últimos 50 registros do Order Book
        cursor.execute("SELECT timestamp, asks, bids FROM order_book ORDER BY id DESC LIMIT 50")
        dados = cursor.fetchall()
        conn.close()

        if not dados:
            logging.warning("⚠️ Nenhum dado de Order Book encontrado!")
            return

        # 🔥 Processar os dados
        timestamps, ask_volumes, bid_volumes = [], [], []

        for row in dados:
            timestamp, asks, bids = row
            asks = json.loads(asks)  # Converter JSON para lista
            bids = json.loads(bids)

            # 📊 Calcular volume total de ASK e BID
            ask_total = sum(float(order[1]) for order in asks)
            bid_total = sum(float(order[1]) for order in bids)

            timestamps.append(timestamp)
            ask_volumes.append(ask_total)
            bid_volumes.append(bid_total)

        # Criar DataFrame
        df = pd.DataFrame({"timestamp": timestamps, "ask_volume": ask_volumes, "bid_volume": bid_volumes})

        # 📊 Calcular o Índice de Liquidez
        df["liquidity_index"] = df["bid_volume"] - df["ask_volume"]

        # 🔥 Pegar o último valor da liquidez
        ultimo_indice = df.iloc[-1]["liquidity_index"]

        # 🔄 Salvar no banco de dados
        conn = sqlite3.connect("data/trading_data.db")
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS liquidity_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp INTEGER,
                liquidity_index REAL
            )
        """)

        cursor.execute("""
            INSERT INTO liquidity_analysis (timestamp, liquidity_index)
            VALUES (?, ?)
        """, (timestamps[-1], ultimo_indice))

        conn.commit()
        conn.close()

        logging.info(f"✅ Índice de Liquidez atualizado: {ultimo_indice}")

    except Exception as e:
        logging.error(f"❌ Erro ao analisar liquidez: {e}")

# 🔄 Loop para rodar continuamente a cada 5 segundos
while True:
    analisar_liquidez()
    time.sleep(5)  # Atualiza a cada 5 segundos
