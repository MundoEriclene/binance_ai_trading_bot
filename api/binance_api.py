import os
import sqlite3
import pandas as pd
import time
from binance.client import Client
from dotenv import load_dotenv

# 🔥 Carregar variáveis de ambiente (.env)
load_dotenv("config/.env")
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

# 📌 Criar cliente da Binance
client = Client(API_KEY, API_SECRET)

# 🔹 Configuração dos ativos e timeframes
SYMBOLS = ["BTCUSDT", "ETHUSDT", "LTCUSDT"]
TIMEFRAME = "5m"
START_DATE = "2017-01-01"
LIMIT = 1000  # 🔥 Limite da Binance por requisição

# 📂 Caminho do banco de dados
DB_PATH = "data/trading_data.db"

# 🔥 Criar conexão com o banco de dados e garantir que as tabelas existem
def setup_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for symbol in SYMBOLS:
        table_name = f"historico_{symbol.lower()}"
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp INTEGER UNIQUE,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume REAL
            )
        """)
        print(f"✅ Tabela `{table_name}` criada/verificada com sucesso!")

    conn.commit()
    conn.close()

# 🔥 Função para buscar dados históricos da Binance em múltiplas requisições
def fetch_klines(symbol, interval, start_str):
    """Busca todos os dados históricos da Binance, lidando com a limitação de 1000 candles por requisição."""
    print(f"📊 Buscando dados completos para {symbol}...")

    all_data = []
    last_timestamp = None

    while True:
        klines = client.get_historical_klines(symbol, interval, start_str, limit=LIMIT)

        if not klines:
            break  # 🔴 Se não houver mais dados, saímos do loop

        for kline in klines:
            all_data.append([
                kline[0],  # timestamp
                float(kline[1]),  # open
                float(kline[2]),  # high
                float(kline[3]),  # low
                float(kline[4]),  # close
                float(kline[5]),  # volume
            ])

        last_timestamp = klines[-1][0]  # Pega o timestamp do último candle baixado
        start_str = str(last_timestamp)  # Atualiza a data inicial para continuar

        print(f"📡 Baixados {len(klines)} novos candles para {symbol}...")

        time.sleep(0.5)  # 🔥 Evitar limitação da API da Binance

    return pd.DataFrame(all_data, columns=["timestamp", "open", "high", "low", "close", "volume"])

# 🔥 Função para salvar os dados no banco de dados
def save_to_db(df, symbol):
    """Salva os dados coletados no banco de dados SQLite"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    table_name = f"historico_{symbol.lower()}"

    # Verificar último timestamp salvo
    cursor.execute(f"SELECT MAX(timestamp) FROM {table_name}")
    last_timestamp = cursor.fetchone()[0]

    if last_timestamp:
        df = df[df["timestamp"] > last_timestamp]  # Apenas novos dados

    if not df.empty:
        df.to_sql(table_name, conn, if_exists="append", index=False)
        print(f"✅ {len(df)} novos registros salvos em {table_name}!")
    else:
        print(f"⚠️ Nenhum novo dado para {symbol}. Banco de dados já está atualizado!")

    conn.commit()
    conn.close()

# 🔥 Configurar o banco de dados antes de buscar os dados
setup_database()

# 🔥 Loop para buscar e salvar dados para cada ativo
for symbol in SYMBOLS:
    print(f"\n📡 Processando {symbol}...")

    try:
        # Pega a data mais recente disponível no banco de dados
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        table_name = f"historico_{symbol.lower()}"

        cursor.execute(f"SELECT MAX(timestamp) FROM {table_name}")
        last_timestamp = cursor.fetchone()[0]
        conn.close()

        # Define a data de início
        if last_timestamp:
            start_date = pd.to_datetime(last_timestamp, unit="ms").strftime("%Y-%m-%d %H:%M:%S")
            print(f"📊 Dados já disponíveis até {last_timestamp}. Buscando apenas novos candles...")
        else:
            start_date = START_DATE
            print(f"⚠️ Nenhum dado encontrado! Baixando desde {START_DATE}...")

        # Baixar os dados da Binance
        df = fetch_klines(symbol, TIMEFRAME, start_date)
        
        if not df.empty:
            save_to_db(df, symbol)

    except Exception as e:
        print(f"❌ Erro ao processar {symbol}: {str(e)}")

print("\n🚀 Processo de coleta de dados finalizado!")
