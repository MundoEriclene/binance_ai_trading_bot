import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from utils import carregar_configuracoes

def enviar_curriculo_teste(destinatario="ericlenedesousa@gmail.com"):
    config = carregar_configuracoes("/Users/programacao/Documents/binance_ai_trading_bot/config/.env")

    msg = MIMEMultipart()
    msg["From"] = f"{config['nome']} <{config['email']}>"
    msg["To"] = destinatario
    msg["Subject"] = "📄 Currículo – Walter Sousa"

    # Corpo do e-mail HTML
    with open(config["mensagem_html"], "r", encoding="utf-8") as f:
        corpo_html = f.read()
    msg.attach(MIMEText(corpo_html, "html"))

    # Anexar PDF
    with open(config["curriculo"], "rb") as f:
        anexo = MIMEApplication(f.read(), _subtype="pdf")
        anexo.add_header("Content-Disposition", "attachment", filename="Curriculo_Walter_Sousa.pdf")
        msg.attach(anexo)

    # Enviar via SMTP
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(config["email"], config["senha"])
            server.send_message(msg)
        print(f"E-mail enviado com sucesso para {destinatario}")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
