import requests
import time
import random
import string
import re

MAIL_TM_API = "https://api.mail.tm"

def gerar_usuario_senha():
    user = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    senha = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    return user, senha

def criar_email_mailtm():
    dominios = requests.get(f"{MAIL_TM_API}/domains").json().get("hydra:member", [])
    if not dominios:
        raise Exception("❌ Nenhum domínio disponível no mail.tm")

    dominio = dominios[0]["domain"]
    usuario, senha = gerar_usuario_senha()
    email = f"{usuario}@{dominio}"

    print(f"\n📨 Criando conta: {email}")
    r = requests.post(f"{MAIL_TM_API}/accounts", json={"address": email, "password": senha})
    if r.status_code not in [200, 201]:
        raise Exception(f"❌ Falha ao criar conta: {r.text}")

    r_login = requests.post(f"{MAIL_TM_API}/token", json={"address": email, "password": senha})
    token = r_login.json().get("token")
    if not token:
        raise Exception("❌ Token de autenticação não recebido.")

    return email, token

def monitorar_emails(token):
    headers = {"Authorization": f"Bearer {token}"}
    vistos = set()

    print("👂 Aguardando mensagens... Pressione CTRL+C para parar.\n")
    try:
        while True:
            inbox = requests.get(f"{MAIL_TM_API}/messages", headers=headers).json()
            mensagens = inbox.get("hydra:member", [])

            for msg in mensagens:
                if msg["id"] not in vistos:
                    vistos.add(msg["id"])
                    r = requests.get(f"{MAIL_TM_API}/messages/{msg['id']}", headers=headers).json()
                    print("───────────────────────────────────────────")
                    print(f"📩 Novo email!")
                    print(f"👤 De: {r.get('from', {}).get('address', 'Desconhecido')}")
                    print(f"🧾 Assunto: {r.get('subject')}")
                    print(f"📬 Corpo:\n{r.get('text')}")
            time.sleep(3)

    except KeyboardInterrupt:
        print("\n🛑 Monitoramento encerrado pelo usuário.")

if __name__ == "__main__":
    email, token = criar_email_mailtm()
    print(f"\n🚨 Envie emails para: {email}")
    monitorar_emails(token)
