# scripts/nome_aleatorio.py

import random
import os

ARQUIVO_BASE = "../pelotoes/nomes_completos.txt"
ARQUIVO_USADOS = "../pelotoes/nomes_usados.txt"

def gerar_nome_unico():
    os.makedirs(os.path.dirname(ARQUIVO_USADOS), exist_ok=True)

    # Verifica se o arquivo base existe
    if not os.path.exists(ARQUIVO_BASE):
        raise Exception("❌ Arquivo 'nomes_completos.txt' não encontrado.")

    # Carrega nomes da base
    with open(ARQUIVO_BASE, "r") as f:
        todos = [l.strip() for l in f.readlines() if l.strip()]

    # Carrega nomes já usados
    usados = set()
    if os.path.exists(ARQUIVO_USADOS):
        with open(ARQUIVO_USADOS, "r") as f:
            usados = set(l.strip() for l in f.readlines())

    # Remove os já usados
    disponiveis = list(set(todos) - usados)
    if not disponiveis:
        raise Exception("🚫 Todos os nomes foram usados. Adicione mais ao arquivo.")

    nome_completo = random.choice(disponiveis)
    nome, sobrenome = nome_completo.split(" ", 1)

    # Salva o nome como usado
    with open(ARQUIVO_USADOS, "a") as f:
        f.write(nome_completo + "\n")

    return nome, sobrenome

# Gera uma variação sem ponto, para perfis ou exibição
def gerar_nome_variado(nome, sobrenome):
    opcoes = [
        f"{nome} {sobrenome}",              # Padrão
        f"{sobrenome} {nome}",              # Invertido
        f"{nome.lower()}_{sobrenome.lower()}",  # estilo id
        f"{nome.lower()}{sobrenome.lower()}",   # junto
        f"{sobrenome.lower()}{nome.lower()}"    # invertido junto
    ]
    return random.choice(opcoes)
