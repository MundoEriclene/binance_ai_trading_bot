import sqlite3
import pandas as pd

# Conectar ao banco de dados
conn = sqlite3.connect("data/trading_data.db")

# 🔍 Verificar se as tabelas estão vazias
df_price = pd.read_sql_query("SELECT * FROM historico_m5 LIMIT 5", conn)
df_liquidity = pd.read_sql_query("SELECT * FROM liquidity_analysis LIMIT 5", conn)

conn.close()

# Exibir os resultados
print("\n📊 Dados em 'historico_m5':")
print(df_price)

print("\n📊 Dados em 'liquidity_analysis':")
print(df_liquidity)
