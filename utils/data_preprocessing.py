import sqlite3
import pandas as pd

# Conectar ao banco de dados SQLite
conn = sqlite3.connect("data/trading_data.db")
cursor = conn.cursor()

# Carregar os dados
df = pd.read_sql_query("SELECT * FROM historico", conn)

# Fechar conexão
conn.close()

# Converter timestamp para data legível
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

# Remover valores nulos
df.dropna(inplace=True)

# Remover valores negativos (caso existam)
df = df[(df['open'] > 0) & (df['high'] > 0) & (df['low'] > 0) & (df['close'] > 0) & (df['volume'] > 0)]

# Salvar os dados processados
df.to_csv("data/processed/historico_tratado.csv", index=False)

# Exibir as primeiras linhas
print(df.head())
