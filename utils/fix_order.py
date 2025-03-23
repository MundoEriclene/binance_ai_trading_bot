import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect("data/trading_data.db")
cursor = conn.cursor()

# Criar uma tabela temporária ordenada
cursor.execute("""
    CREATE TABLE IF NOT EXISTS historico_m5_temp AS
    SELECT * FROM historico_m5 ORDER BY timestamp ASC
""")

# Remover a tabela original e renomear a nova tabela corretamente
cursor.execute("DROP TABLE historico_m5")
cursor.execute("ALTER TABLE historico_m5_temp RENAME TO historico_m5")

# Salvar as mudanças
conn.commit()
conn.close()

print("✅ Banco de dados reorganizado com sucesso!")
