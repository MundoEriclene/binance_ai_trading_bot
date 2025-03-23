import sqlite3

# 🔥 Conectar ao banco de dados
conn = sqlite3.connect("data/trading_data.db")
cursor = conn.cursor()

# 🔍 Listar todas as tabelas no banco de dados
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

# 🚨 Apagar todas as tabelas
for table in tables:
    table_name = table[0]
    cursor.execute(f"DELETE FROM {table_name}")  # Apaga todos os dados
    cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table_name}'")  # Reseta IDs

conn.commit()
conn.close()

print("✅ Todas as tabelas foram limpas com sucesso!")
