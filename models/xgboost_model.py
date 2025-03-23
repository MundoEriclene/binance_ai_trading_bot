import numpy as np
import pandas as pd
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import xgboost as xgb
import matplotlib.pyplot as plt

# 🔥 1. Carregar os dados do SQLite
conn = sqlite3.connect("data/trading_data.db")
df = pd.read_sql_query("SELECT timestamp, close FROM historico", conn)
conn.close()

# Converter timestamp para datetime
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
df.set_index("timestamp", inplace=True)

# 🔥 2. Normalizar os preços (entre 0 e 1)
scaler = MinMaxScaler(feature_range=(0, 1))
df["close"] = scaler.fit_transform(df["close"].values.reshape(-1, 1))

# 🔥 3. Criar dataset para XGBoost (usando preços passados como features)
look_back = 50
X, y = [], []

for i in range(len(df) - look_back):
    X.append(df["close"].values[i : i + look_back])
    y.append(df["close"].values[i + look_back])

X, y = np.array(X), np.array(y)

# 🔥 4. Dividir os dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# 🔥 5. Criar o modelo XGBoost
model = xgb.XGBRegressor(objective="reg:squarederror", n_estimators=100, learning_rate=0.1)

# 🔥 6. Treinar o modelo
print("Treinando o modelo XGBoost...")
model.fit(X_train, y_train)

# 🔥 7. Avaliar o modelo
y_pred = model.predict(X_test)

# 🔥 8. Visualizar resultados
plt.figure(figsize=(12, 6))
plt.plot(y_test, label="Real")
plt.plot(y_pred, label="Previsto")
plt.title("Previsão XGBoost vs Real")
plt.legend()
plt.show()
