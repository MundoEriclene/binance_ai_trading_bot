import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
import sqlite3
import os
import json

# 🔥 Criar ou carregar o modelo atualizado
model_path = "models/lstm_liquidity_model.keras"
if os.path.exists(model_path):
    print("✅ Modelo existente encontrado! Treinando com novos dados...")
    model = tf.keras.models.load_model(model_path)
else:
    print("⚠️ Nenhum modelo encontrado! Criando um novo modelo...")
    
    # Criar um novo modelo LSTM com liquidez e volume
    model = Sequential([
        LSTM(32, return_sequences=True, input_shape=(50, 4)),  # Agora temos 4 inputs
        Dropout(0.3),
        LSTM(32, return_sequences=False),
        Dropout(0.3),
        Dense(16, activation="relu"),
        Dense(1)
    ])
    model.compile(optimizer="adam", loss="mean_squared_error")

# 🔥 Conectar ao banco de dados e carregar os dados
conn = sqlite3.connect("data/trading_data.db")
df_price = pd.read_sql_query("SELECT timestamp, close, volume FROM historico_m5", conn)
df_liquidity = pd.read_sql_query("SELECT timestamp, liquidity_index FROM liquidity_analysis", conn)
conn.close()

# Converter timestamp para datetime
df_price["timestamp"] = pd.to_datetime(df_price["timestamp"], unit="ms")
df_liquidity["timestamp"] = pd.to_datetime(df_liquidity["timestamp"], unit="ms")

# 🔄 Juntar os dados pelo timestamp
df = pd.merge(df_price, df_liquidity, on="timestamp", how="left")
df["liquidity_index"] = df["liquidity_index"].ffill().fillna(0)

# 📊 Normalizar os dados
scaler = MinMaxScaler(feature_range=(0, 1))
df[["close", "liquidity_index", "volume"]] = scaler.fit_transform(df[["close", "liquidity_index", "volume"]])

# Criar coluna de Média Móvel de Liquidez
df["liquidity_ma"] = df["liquidity_index"].rolling(window=5).mean()
df.dropna(inplace=True)

# 🔥 Criar dataset para o modelo
def criar_dados_lstm(dataset, look_back=50):
    X, y = [], []
    for i in range(len(dataset) - look_back):
        X.append(dataset[i : i + look_back])
        y.append(dataset[i + look_back, 0])
    return np.array(X), np.array(y)

data = df[["close", "liquidity_index", "volume", "liquidity_ma"]].values
X, y = criar_dados_lstm(data)

train_size = int(len(X) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# 🔥 Treinar o modelo
print("🚀 Treinando o modelo com dados de liquidez e volume...")
history = model.fit(X_train, y_train, batch_size=32, epochs=20, validation_data=(X_test, y_test))

# 🔄 Salvar o modelo atualizado
model.save(model_path)
print("✅ Modelo treinado e salvo com sucesso!")

# 🔥 Salvar histórico do treinamento
history_dict = {"loss": history.history["loss"], "val_loss": history.history["val_loss"]}
with open("models/training_history.json", "w") as f:
    json.dump(history_dict, f)
print("✅ Histórico do treinamento salvo!")
