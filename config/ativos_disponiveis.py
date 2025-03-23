import requests
import json

API_URL = "https://yobit.net/api/3/info"

def get_all_pairs():
    """ Obtém todos os pares de negociação disponíveis na Yobit """
    try:
        response = requests.get(API_URL)
        data = response.json()
        return list(data["pairs"].keys())
    except Exception as e:
        print(f"❌ Erro ao obter lista de ativos: {e}")
        return []

# Salva a lista de ativos disponíveis para referência futura
pares_disponiveis = get_all_pairs()
with open("pares_disponiveis.json", "w") as f:
    json.dump(pares_disponiveis, f)

print(f"✅ Lista de pares salva ({len(pares_disponiveis)} pares encontrados).")
