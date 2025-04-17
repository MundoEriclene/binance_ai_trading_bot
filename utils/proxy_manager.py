import os
import random

PROXY_ARQUIVO = 'config/proxies.txt'
PROXIES_USADOS = 'logs/proxies_usados.txt'

def carregar_proxies(caminho):
    if not os.path.exists(caminho):
        return set()
    with open(caminho, 'r', encoding='utf-8') as f:
        return {linha.strip() for linha in f if linha.strip()}

def salvar_proxy_usado(proxy):
    with open(PROXIES_USADOS, 'a', encoding='utf-8') as f:
        f.write(proxy + '\n')

def escolher_proxy():
    todos = carregar_proxies(PROXY_ARQUIVO)
    usados = carregar_proxies(PROXIES_USADOS)

    disponiveis = list(todos - usados)

    if not disponiveis:
        raise Exception("❌ Todos os proxies disponíveis já foram usados.")

    proxy_escolhido = random.choice(disponiveis)
    salvar_proxy_usado(proxy_escolhido)
    return proxy_escolhido

# Teste
if __name__ == "__main__":
    proxy = escolher_proxy()
    print(f"🌐 Proxy escolhido: {proxy}")
