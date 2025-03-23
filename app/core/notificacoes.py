import os
import requests
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# === VARIÁVEIS DE AMBIENTE ===
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_DESTINO = os.getenv("EMAIL_DESTINO")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_IDS = [
    os.getenv("TELEGRAM_CHAT_ID_CANAL"),
    os.getenv("TELEGRAM_CHAT_ID_PESSOAL")
]

# === ENVIO DE EMAIL ===
def enviar_email(assunto, mensagem):
    if not all([EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_DESTINO]):
        print("⚠️ Dados de e-mail incompletos. Verifique .env.")
        return

    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_DESTINO
        msg["Subject"] = assunto
        msg.attach(MIMEText(mensagem, "plain"))
        contexto = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_DESTINO, msg.as_string())

    except Exception as e:
        print(f"❌ Erro ao enviar e-mail: {e}")

# === ENVIO DE TELEGRAM ===
def enviar_telegram(mensagem):
    if not TELEGRAM_TOKEN:
        print("⚠️ Token do Telegram ausente.")
        return

    for chat_id in TELEGRAM_CHAT_IDS:
        if chat_id:
            try:
                url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
                payload = {
                    "chat_id": chat_id,
                    "text": mensagem,
                    "parse_mode": "Markdown"
                }
                response = requests.post(url, data=payload)
                if response.status_code != 200:
                    print(f"❌ Falha Telegram [{chat_id}]: {response.text}")
            except Exception as e:
                print(f"❌ Erro no Telegram ({chat_id}): {e}")

# === USO EM ERROS ===
def reportar_erro(msg):
    erro_formatado = f"❌ ERRO DETECTADO:\n{msg}"
    enviar_telegram(erro_formatado)
    enviar_email("❌ ERRO no RoboTrader", msg)
