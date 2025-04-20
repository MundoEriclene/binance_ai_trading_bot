# email_sender.py

import smtplib
import ssl
from email.message import EmailMessage
from config import CONFIG

def enviar_email(destinatario: str) -> bool:
    try:
        # Lê o corpo do email padrão
        with open(CONFIG["mensagem_email_path"], "r", encoding="utf-8") as f:
            corpo_email = f.read()

        # Cria o objeto do email
        msg = EmailMessage()
        msg["Subject"] = "Candidatura à vaga Comercial"
        msg["From"] = CONFIG["email_envio"]
        msg["To"] = destinatario
        msg.set_content(corpo_email)

        # Anexa o currículo PDF
        with open(CONFIG["curriculo_path"], "rb") as pdf:
            msg.add_attachment(pdf.read(), maintype="application", subtype="pdf", filename="Curriculo_Ericlene.pdf")

        # Envia o e-mail via Gmail SMTP
        contexto = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto) as smtp:
            smtp.login(CONFIG["email_envio"], CONFIG["email_senha"])
            smtp.send_message(msg)

        print(f"[✓] E-mail enviado para: {destinatario}")
        return True

    except Exception as e:
        print(f"[✗] Falha ao enviar para {destinatario}: {e}")
        return False
