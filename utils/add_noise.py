import pandas as pd
import numpy as np
import os

# 📂 Caminho dos arquivos CSV
train_path = "data/processed/train_data.csv"
val_path = "data/processed/val_data.csv"
test_path = "data/processed/test_data.csv"

# 📌 Carregar os dados
df_train = pd.read_csv(train_path)
df_val = pd.read_csv(val_path)
df_test = pd.read_csv(test_path)

# 📌 Adicionar ruído aleatório simulado no preço de fechamento
def add_noise(data, noise_level=0.02):
    noise = np.random.normal(0, noise_level, size=data["close"].shape)  # Ruído normal com média 0 e desvio padrão de 2%
    data["close"] = data["close"] * (1 + noise)
    return data

df_train = add_noise(df_train, noise_level=0.02)  # 2% de ruído no treino
df_val = add_noise(df_val, noise_level=0.02)  # 2% de ruído na validação
df_test = add_noise(df_test, noise_level=0.02)  # 2% de ruído no teste

# 💾 Salvar os novos arquivos com ruído
df_train.to_csv("data/processed/train_data_noisy.csv", index=False)
df_val.to_csv("data/processed/val_data_noisy.csv", index=False)
df_test.to_csv("data/processed/test_data_noisy.csv", index=False)

print("✅ Dados com ruído salvos com sucesso!")
