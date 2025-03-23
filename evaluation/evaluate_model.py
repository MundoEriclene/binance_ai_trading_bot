import numpy as np
import pandas as pd
import sqlite3
import tensorflow as tf
from sklearn.metrics import mean_squared_error, mean_absolute_error

# 🔥 Conectar ao banco de dados e carregar os dados
conn = sqlite3.connect("data/trading_data.db")

# Pegar os dados de preços e liquidez
df_price = pd.read_sql_query("SELECT timestamp, close FROM historico_m5", conn)
df_liquidity = pd.read_sql_query("SELECT timestamp, liquidity_index FROM liquidity_analysis", conn)
conn.close()

# Converter timestamp para datetime
df_price["timestamp"] = pd.to_datetime(df_price["timestamp"], unit="ms")
df_liquidity["timestamp"] = pd.to_datetime(df_liquidity["timestamp"], unit="ms")

# 🔄 Juntar os dados
df = pd.merge(df_price, df_liquidity, on="timestamp", how="left")
df["liquidity_index"].fillna(method="ffill", inplace=True)
df["liquidity_index"].fillna(0, inplace=True)

# 📊 Normalizar os dados
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0, 1))
df[["close", "liquidity_index"]] = scaler.fit_transform(df[["close", "liquidity_index"]])

# Criar colunas auxiliares
df["liquidity_ma"] = df["liquidity_index"].rolling(window=5).mean()
df.dropna(inplace=True)

# 🔥 Criar dataset para avaliação
def criar_dados_lstm(dataset, look_back=50):
    X, y = [], []
    for i in range(len(dataset) - look_back):
        X.append(dataset[i : i + look_back])
        y.append(dataset[i + look_back, 0])  # Prevendo preço de fechamento
    return np.array(X), np.array(y)

data = df[["close", "liquidity_index", "liquidity_ma"]].values
X, y = criar_dados_lstm(data)

# 🔄 Dividir os dados em treino e teste
train_size = int(len(X) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# 🔥 Carregar o modelo treinado
model_path = "models/lstm_liquidity_model.h5"
model = tf.keras.models.load_model(model_path)

# 📊 Fazer previsões no conjunto de teste
y_pred = model.predict(X_test)

# 🔥 Avaliação do modelo
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)

# 📊 Acurácia da Direção (quantas vezes acertamos se o preço subiria ou cairia)
direction_accuracy = np.mean((y_pred[:-1] > y_pred[1:]) == (y_test[:-1] > y_test[1:])) * 100

# 📊 Exibir os resultados
print("\n📊 RESULTADOS DA AVALIAÇÃO:")
print(f"📉 Erro Médio Quadrático (MSE): {mse:.6f}")
print(f"📉 Erro Absoluto Médio (MAE): {mae:.6f}")
print(f"🎯 Acurácia das Direções: {direction_accuracy:.2f}%")
