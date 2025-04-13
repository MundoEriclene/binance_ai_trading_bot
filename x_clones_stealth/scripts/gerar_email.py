# scripts/gerar_email.py

import random
import string
import os

# Caminho onde serão armazenados os e-mails gerados
EMAILS_USADOS_PATH = "../pelotoes/emails_gerados.txt"

def gerar_email():
    os.makedirs(os.path.dirname(EMAILS_USADOS_PATH), exist_ok=True)
    usados = set()

    # Lê e-mails já usados
    if os.path.exists(EMAILS_USADOS_PATH):
        with open(EMAILS_USADOS_PATH, "r") as f:
            usados = set(l.strip() for l in f.readlines())

    # Gera um novo email até que seja único
    while True:
        alias = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        email = f"{alias}@blacknode.quest"
        if email not in usados:
            break

    # Salva o novo e-mail
    with open(EMAILS_USADOS_PATH, "a") as f:
        f.write(email + "\n")

    return email
