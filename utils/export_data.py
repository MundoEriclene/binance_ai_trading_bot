import sqlite3
import pandas as pd

# Conectar ao banco SQLite
conn = sqlite3.connect("data/trading_data.db")

# Carregar os dados de M5
df_m5 = pd.read_sql_query("SELECT * FROM historico_m5", conn)

# Carregar os dados de M30
df_m30 = pd.read_sql_query("SELECT * FROM historico_m30", conn)

# Fechar conexão
conn.close()

# Converter timestamp para data legível
df_m5["timestamp"] = pd.to_datetime(df_m5["timestamp"], unit="ms")
df_m30["timestamp"] = pd.to_datetime(df_m30["timestamp"], unit="ms")

# Salvar os arquivos CSV na pasta data/processed/
df_m5.to_csv("data/processed/historico_m5.csv", index=False)
df_m30.to_csv("data/processed/historico_m30.csv", index=False)

print("📂 Dados exportados para data/processed/")
