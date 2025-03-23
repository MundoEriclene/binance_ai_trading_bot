import sqlite3
import pandas as pd

# 🔥 Conectar ao banco de dados
conn = sqlite3.connect("data/trading_data.db")
cursor = conn.cursor()

# 🔍 Listar todas as tabelas no banco de dados
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print("\n📊 Tabelas no banco de dados:")
for table in tables:
    table_name = table[0]
    print(f"\n🔹 Dados na tabela: {table_name}")
    
    # Carregar os dados da tabela e exibir os 5 primeiros registros
    df = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT 5", conn)
    print(df)

conn.close()
