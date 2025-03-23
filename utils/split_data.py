import sqlite3
import pandas as pd
import os

# 📂 Caminho correto do banco de dados
DB_PATH = os.path.join(os.path.dirname(__file__), "../data/trading_data.db")

# 🔥 Conectar ao banco e carregar os dados
conn = sqlite3.connect(DB_PATH)
df = pd.read_sql_query("SELECT * FROM historico_m5", conn)
conn.close()

# 📌 Converter timestamp para formato de data
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

# 🔄 Separar os períodos corretamente
df_train = df[df["timestamp"] < "2023-01-01"]
df_val = df[(df["timestamp"] >= "2023-01-01") & (df["timestamp"] < "2024-01-01")]
df_test = df[df["timestamp"] >= "2024-01-01"]

# 📂 Criar diretório para salvar os arquivos CSV se não existir
os.makedirs("data/processed", exist_ok=True)

# 💾 Salvar separadamente
df_train.to_csv("data/processed/train_data.csv", index=False)
df_val.to_csv("data/processed/val_data.csv", index=False)
df_test.to_csv("data/processed/test_data.csv", index=False)

print(f"✅ Dados separados:\n- Treino: {len(df_train)} registros\n- Validação: {len(df_val)} registros\n- Teste: {len(df_test)} registros")
