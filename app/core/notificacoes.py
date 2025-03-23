import os
import requests
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_DESTINO = os.getenv("EMAIL_DESTINO")

def enviar_email(assunto, mensagem):
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
        print(f"Erro ao enviar e-mail: {e}")

def enviar_telegram(mensagem):
    token = os.getenv("TELEGRAM_TOKEN")
    ids = [
        os.getenv("TELEGRAM_CHAT_ID_CANAL"),
        os.getenv("TELEGRAM_CHAT_ID_PESSOAL")
    ]

    for chat_id in ids:
        if chat_id:
            try:
                url = f"https://api.telegram.org/bot{token}/sendMessage"
                payload = {
                    "chat_id": chat_id,
                    "text": mensagem,
                    "parse_mode": "Markdown"
                }
                response = requests.post(url, data=payload)
                if response.status_code != 200:
                    print(f"Erro ao enviar para {chat_id}: {response.text}")
            except Exception as e:
                print(f"Erro no Telegram ({chat_id}): {e}")
def reportar_erro(msg):
    enviar_telegram(f"❌ ERRO DETECTADO:\n{msg}")
    enviar_email("❌ ERRO no RoboTrader", msg)
