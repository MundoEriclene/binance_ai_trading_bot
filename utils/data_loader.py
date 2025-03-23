import sqlite3
import pandas as pd

# Conectar ao banco de dados SQLite
conn = sqlite3.connect("data/trading_data.db")
cursor = conn.cursor()

# Carregar os dados
df = pd.read_sql_query("SELECT * FROM historico", conn)

# Fechar a conexão
conn.close()

# Exibir as primeiras linhas
print(df.head())
