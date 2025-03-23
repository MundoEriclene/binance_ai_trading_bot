import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam

# 📂 Caminho dos arquivos CSV já separados
train_path = "data/processed/train_data.csv"
val_path = "data/processed/val_data.csv"
test_path = "data/processed/test_data.csv"

# 📌 Carregar os dados
df_train = pd.read_csv(train_path)
df_val = pd.read_csv(val_path)
df_test = pd.read_csv(test_path)

# 📌 Converter timestamp para datetime
df_train["timestamp"] = pd.to_datetime(df_train["timestamp"])
df_val["timestamp"] = pd.to_datetime(df_val["timestamp"])
df_test["timestamp"] = pd.to_datetime(df_test["timestamp"])

# 🔥 Normalizar os dados (MinMaxScaler para escalar os preços)
scaler = MinMaxScaler(feature_range=(0, 1))
df_train[["open", "high", "low", "close", "volume"]] = scaler.fit_transform(df_train[["open", "high", "low", "close", "volume"]])
df_val[["open", "high", "low", "close", "volume"]] = scaler.transform(df_val[["open", "high", "low", "close", "volume"]])
df_test[["open", "high", "low", "close", "volume"]] = scaler.transform(df_test[["open", "high", "low", "close", "volume"]])

# 📌 Função para criar sequências de treino
def create_sequences(data, look_back=50):
    X, y = [], []
    for i in range(len(data) - look_back):
        X.append(data[i : i + look_back, :-1])  # Todas as colunas menos a última (target)
        y.append(data[i + look_back, -2])  # Target: Preço de fechamento
    return np.array(X), np.array(y)

# 📌 Implementação do Walk-Forward Validation
initial_year = 2017
final_year = 2023
look_back = 50  # Número de candles passados usados para prever o próximo

# 🔄 Iterar ano por ano
for year in range(initial_year, final_year):
    print(f"\n🚀 Treinando de {initial_year}-{year} e validando em {year+1}...")

    # 📌 Criar conjunto de treino progressivo
    df_train_progressive = df_train[df_train["timestamp"] < f"{year+1}-01-01"]
    df_val_progressive = df_train[(df_train["timestamp"] >= f"{year+1}-01-01") & (df_train["timestamp"] < f"{year+2}-01-01")]

    # 📌 Transformar os dados para input do modelo
    data_train = df_train_progressive[["open", "high", "low", "close", "volume"]].values
    data_val = df_val_progressive[["open", "high", "low", "close", "volume"]].values

    X_train, y_train = create_sequences(data_train, look_back)
    X_val, y_val = create_sequences(data_val, look_back)

    # 🔥 Criar o modelo LSTM
    model = Sequential([
        LSTM(64, return_sequences=True, input_shape=(look_back, 4)),
        Dropout(0.2),
        LSTM(64, return_sequences=False),
        Dropout(0.2),
        Dense(32, activation="relu"),
        Dense(1)
    ])
    model.compile(optimizer=Adam(learning_rate=0.001), loss="mean_squared_error")

    # 📌 Treinar o modelo
    model.fit(X_train, y_train, epochs=5, batch_size=32, validation_data=(X_val, y_val))

    # 📊 Avaliação
    val_loss = model.evaluate(X_val, y_val)
    print(f"✅ Validação em {year+1} - Perda: {val_loss:.5f}")

print("\n🚀 Walk-Forward Validation concluído!")
