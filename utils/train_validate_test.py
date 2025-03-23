import pandas as pd
import numpy as np
import os
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.regularizers import l2
from sklearn.preprocessing import MinMaxScaler

# 📌 Escolher se queremos usar os dados com ruído ou não
USE_NOISY_DATA = True  # ✅ Altere para False se quiser usar os dados sem ruído

# 📂 Caminhos dos arquivos CSV já separados
if USE_NOISY_DATA:
    train_path = "data/processed/train_data_noisy.csv"
    val_path = "data/processed/val_data_noisy.csv"
    test_path = "data/processed/test_data_noisy.csv"
else:
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

# 🔥 Normalizar os dados
scaler = MinMaxScaler(feature_range=(0, 1))
df_train[["open", "high", "low", "close", "volume"]] = scaler.fit_transform(df_train[["open", "high", "low", "close", "volume"]])
df_val[["open", "high", "low", "close", "volume"]] = scaler.transform(df_val[["open", "high", "low", "close", "volume"]])
df_test[["open", "high", "low", "close", "volume"]] = scaler.transform(df_test[["open", "high", "low", "close", "volume"]])

# 📌 Criar sequências para LSTM
def create_sequences(data, look_back=50):
    X, y = [], []
    for i in range(len(data) - look_back):
        X.append(data[i : i + look_back, :])  # Pegando todas as colunas como entrada
        y.append(data[i + look_back, 3])  # Pegando a coluna de fechamento como target
    return np.array(X), np.array(y).reshape(-1, 1)  # 🚀 Garantindo que `y` seja 2D

# 📌 Criar datasets para treinamento, validação e teste
look_back = 50
X_train, y_train = create_sequences(df_train[["open", "high", "low", "close", "volume"]].values, look_back)
X_val, y_val = create_sequences(df_val[["open", "high", "low", "close", "volume"]].values, look_back)
X_test, y_test = create_sequences(df_test[["open", "high", "low", "close", "volume"]].values, look_back)

# 🔥 Criar o modelo LSTM com regularização L2
model = Sequential([
    LSTM(64, return_sequences=True, input_shape=(look_back, 5), kernel_regularizer=l2(0.001)),  # Regularização L2
    Dropout(0.2),
    LSTM(64, return_sequences=False, kernel_regularizer=l2(0.001)),  # Regularização L2 na segunda camada
    Dropout(0.2),
    Dense(32, activation="relu", kernel_regularizer=l2(0.001)),  # Regularização L2 na camada densa
    Dense(1)
])
model.compile(optimizer=Adam(learning_rate=0.001), loss="mean_squared_error")

# 📌 Early Stopping para evitar overfitting
early_stopping = EarlyStopping(monitor="val_loss", patience=3, restore_best_weights=True)

# 📌 Treinar o modelo
print("\n🚀 Treinando o modelo com dados de 2017-2022...")
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_val, y_val), callbacks=[early_stopping])

# 📊 Avaliação no conjunto de teste (2024-2025)
print("\n🚀 Testando o modelo com dados de 2024-2025...")
test_loss = model.evaluate(X_test, y_test)
print(f"✅ Teste final concluído - Perda: {test_loss:.5f}")

# 💾 Salvar modelo treinado
model.save("models/lstm_trained.h5")
print("✅ Modelo treinado e salvo com sucesso!")
