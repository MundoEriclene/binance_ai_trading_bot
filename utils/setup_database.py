import sqlite3
import os

# 📂 Caminho correto para o banco de dados
DB_PATH = os.path.join(os.path.dirname(__file__), "../data/trading_data.db")

# 🔥 Conectar ao banco e criar tabelas
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Criar tabela de candles M5
cursor.execute("""
    CREATE TABLE IF NOT EXISTS historico_m5 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp INTEGER UNIQUE,
        open REAL,
        high REAL,
        low REAL,
        close REAL,
        volume REAL
    )
""")

# Criar tabela de liquidez
cursor.execute("""
    CREATE TABLE IF NOT EXISTS liquidity_analysis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp INTEGER UNIQUE,
        liquidity_index REAL
    )
""")

conn.commit()
conn.close()

print("✅ Banco de dados recriado com sucesso!")
