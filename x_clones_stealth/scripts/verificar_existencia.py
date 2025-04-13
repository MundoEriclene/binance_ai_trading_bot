# scripts/verificar_existencia.py

import os

def email_ja_usado(pelotao_id, email):
    caminho = f"../pelotoes/pelotao_{str(pelotao_id).zfill(2)}/contas.txt"
    if not os.path.exists(caminho):
        return False

    with open(caminho, "r") as f:
        linhas = f.readlines()

    for linha in linhas:
        if email in linha:
            return True
    return False

def nome_ja_usado(nome_completo):
    caminho = "../pelotoes/nomes_usados.txt"
    if not os.path.exists(caminho):
        return False

    with open(caminho, "r") as f:
        usados = set(l.strip() for l in f.readlines())

    return nome_completo in usados
