import os
import sqlite3
import logging
import dotenv
from binance.client import Client
import time
import json

# 🔥 Carregar variáveis de ambiente do arquivo .env
dotenv.load_dotenv("config/.env")

# 🔑 Pegar chaves de API da Binance do .env
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

# 🚀 Conectar à Binance de forma segura
client = Client(API_KEY, API_SECRET)

# 🔥 Configurar Diretório e Arquivos de Log
log_dir = "logs"
log_file = f"{log_dir}/order_book.log"
error_file = f"{log_dir}/errors.log"

# Criar diretório de logs se não existir
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Configurar logs de informação
logging.basicConfig(level=logging.INFO, filename=log_file, filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s")

# 🔥 Criar Banco de Dados para Order Book
conn = sqlite3.connect("data/trading_data.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_book (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp INTEGER,
        asks TEXT,
        bids TEXT
    )
""")

conn.commit()
conn.close()

# 🔄 Função para coletar e salvar o order book
def coletar_order_book(par="BTCUSDT"):
    """
    Coleta o livro de ofertas (Order Book) da Binance e salva no banco de dados.
    """
    try:
        # 📊 Obter o Order Book
        order_book = client.get_order_book(symbol=par, limit=20)  # Pegamos os 20 melhores preços

        # 🔥 Processar e salvar no banco
        timestamp = int(time.time() * 1000)
        asks = json.dumps(order_book["asks"])  # Lista de ordens de venda
        bids = json.dumps(order_book["bids"])  # Lista de ordens de compra

        conn = sqlite3.connect("data/trading_data.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO order_book (timestamp, asks, bids)
            VALUES (?, ?, ?)
        """, (timestamp, asks, bids))

        conn.commit()
        conn.close()
        logging.info("✅ Order Book salvo com sucesso!")

    except Exception as e:
        logging.error(f"❌ Erro ao coletar Order Book: {e}")

# 🔄 Loop para coletar order book a cada 5 segundos
while True:
    coletar_order_book()
    time.sleep(5)  # Coleta dados a cada 5 segundos
