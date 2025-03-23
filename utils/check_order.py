import sqlite3
import pandas as pd

# Conectar ao banco de dados
conn = sqlite3.connect("data/trading_data.db")

# Pegar os primeiros e últimos 10 registros para ver se estão ordenados
df = pd.read_sql_query("SELECT * FROM historico_m5 ORDER BY timestamp LIMIT 10", conn)
print("\n📊 PRIMEIROS 10 DADOS:")
print(df)

df = pd.read_sql_query("SELECT * FROM historico_m5 ORDER BY timestamp DESC LIMIT 10", conn)
print("\n📊 ÚLTIMOS 10 DADOS:")
print(df)

conn.close()
