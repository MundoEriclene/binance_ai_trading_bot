import requests
import time
import random
import string
import os

def gerar_email():
    nome = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    dominio = "mail.socio"
    return f"{nome}@{dominio}"

def monitorar_email(destinatario):
    print(f"\n📡 Monitorando e-mail: {destinatario}")
    print("Aguarde mensagens... (Ctrl+C para sair)\n")

    mensagens_anteriores = set()

    try:
        while True:
            resposta = requests.get("http://localhost:8025/api/v2/messages")
            mensagens = resposta.json()["items"]

            for msg in mensagens:
                destinatarios = msg["To"]
                if any(destinatario in to["Mailbox"] + "@" + to["Domain"] for to in destinatarios):
                    msg_id = msg["ID"]
                    if msg_id not in mensagens_anteriores:
                        assunto = msg["Content"]["Headers"].get("Subject", ["(Sem assunto)"])[0]
                        corpo = msg["Content"]["Body"]

                        print("📨 Nova mensagem recebida:")
                        print(f"📥 Assunto: {assunto}")
                        print(f"🧾 Corpo:\n{corpo}\n")
                        print("="*60)
                        mensagens_anteriores.add(msg_id)

            time.sleep(2)

    except KeyboardInterrupt:
        print("\n🛑 Monitoramento encerrado pelo usuário.")

if __name__ == "__main__":
    os.system("clear" if os.name == "posix" else "cls")
    email = gerar_email()
    print(f"✅ E-mail gerado: {email}")
    print("📬 Envie uma mensagem para este e-mail usando o Gmail ou outro provedor.")
    monitorar_email(email)
