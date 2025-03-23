import matplotlib.pyplot as plt
import json

# 🔥 Carregar histórico do treinamento
with open("models/training_history.json", "r") as f:
    history = json.load(f)

# 📊 Plotar Loss e Val_Loss
plt.figure(figsize=(10, 5))
plt.plot(history["loss"], label="Treinamento")
plt.plot(history["val_loss"], label="Teste")
plt.xlabel("Épocas")
plt.ylabel("Loss")
plt.legend()
plt.title("Verificação de Overfitting")
plt.show()
