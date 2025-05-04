import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
from dotenv import load_dotenv
from pathlib import Path

# ⚙️ Carregar o .env do diretório config/
load_dotenv(dotenv_path=Path(__file__).parent / "config" / ".env")

# Variáveis do ambiente
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_DESTINO = os.getenv("EMAIL_DESTINO")
DATA_INICIAL = datetime.strptime(os.getenv("DATA_INICIAL"), "%Y-%m-%d")
DATA_FINAL = datetime.strptime(os.getenv("DATA_FINAL"), "%Y-%m-%d")
AGORA = datetime.now()

# Cálculos de progresso
segundos_totais = (DATA_FINAL - DATA_INICIAL).total_seconds()
segundos_passados = (AGORA - DATA_INICIAL).total_seconds()
segundos_restantes = max((DATA_FINAL - AGORA).total_seconds(), 0)

# Porcentagem real
porcentagem = round(min(100.0, max(0.0, (segundos_passados / segundos_totais) * 100)), 2)

# Dias e horas restantes
dias_restantes = int(segundos_restantes // (3600 * 24))
horas_restantes = int((segundos_restantes % (3600 * 24)) // 3600)

# Atualizar HTML
with open("template_email.html", "r", encoding="utf-8") as f:
    html = f.read()
    html = html.replace("{{dias_restantes}}", str(dias_restantes))
    html = html.replace("{{horas_restantes}}", str(horas_restantes))
    html = html.replace("{{porcentagem}}", str(porcentagem))
    html = html.replace("{{data_final_js}}", DATA_FINAL.strftime("%Y-%m-%dT%H:%M:%S"))

# Enviar e-mail
msg = MIMEMultipart("alternative")
msg["Subject"] = "📅 Contagem para Liberdade"
msg["From"] = EMAIL_USERNAME
msg["To"] = EMAIL_DESTINO
msg.attach(MIMEText(html, "html"))

try:
    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    server.starttls()
    server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
    server.sendmail(EMAIL_USERNAME, EMAIL_DESTINO, msg.as_string())
    server.quit()
    print("E-mail enviado com sucesso!")
except Exception as e:
    print("Erro ao enviar e-mail:", e)
