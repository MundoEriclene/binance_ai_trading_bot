import smtplib
import os
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
import csv
import time

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv('/Users/programacao/documents/binance_ai_trading_bot/config/.env')

# Carregar os dados do Gmail do arquivo .env
GMAIL_USER = os.getenv('GMAIL_USER')
GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD')

# Função para verificar se o email tem o formato válido (usando expressão regular)
def validar_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(regex, email):
        return True
    else:
        print(f"Email inválido: {email}")
        return False

# Função para verificar se o email já foi enviado
def verificar_email_enviado(email):
    if not os.path.exists('/Users/programacao/documents/binance_ai_trading_bot/job_hunter_netempregos/emails_enviados.csv'):
        with open('/Users/programacao/documents/binance_ai_trading_bot/job_hunter_netempregos/emails_enviados.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Email"])  # Cabeçalho para o CSV

    with open('/Users/programacao/documents/binance_ai_trading_bot/job_hunter_netempregos/emails_enviados.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == email:
                return True
    return False

# Função para registrar o email como enviado
def registrar_email_enviado(email):
    with open('/Users/programacao/documents/binance_ai_trading_bot/job_hunter_netempregos/emails_enviados.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([email])

# Função para enviar o email
def send_email(to_email):
    # Verificar se o email é válido
    if not validar_email(to_email):
        return  # Não enviar se o email for inválido

    # Criar a mensagem
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = to_email
    msg['Subject'] = 'Candidatura - Vaga Comercial'

    # Corpo do email (HTML)
    body = """
    <!DOCTYPE html>
    <html lang="pt">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Candidatura - Vaga Comercial</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                margin: 0;
                padding: 0;
                background-color: #101010;
                color: #FFFFFF;
            }
            .email-container {
                width: 100%;
                max-width: 700px;
                margin: 0 auto;
                padding: 40px;
                background-color: #181818;
                border-radius: 10px;
                box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.3);
                text-align: center;
            }
            .header {
                font-size: 32px;
                font-weight: bold;
                color: #00FF99;
                margin-bottom: 20px;
            }
            .content {
                font-size: 18px;
                line-height: 1.6;
                margin-bottom: 30px;
                color: #CCCCCC;
            }
            .cta-button {
                padding: 16px 30px;
                background-color: #00D4B8;
                color: #FFFFFF;
                font-size: 18px;
                font-weight: bold;
                text-decoration: none;
                border-radius: 50px;
                transition: background-color 0.3s ease, transform 0.3s ease;
            }
            .cta-button:hover {
                background-color: #008C6D;
                transform: scale(1.05);
            }
            .footer {
                margin-top: 40px;
                font-size: 14px;
                color: #888888;
            }
            .footer a {
                color: #00FF99;
                text-decoration: none;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">
                Olá, Recrutador!
            </div>
            <div class="content">
                <p>Sou Ericlene De Sousa, um profissional focado em gerar resultados e liderar iniciativas comerciais com precisão.</p>
                <p>Com anos de experiência em vendas e desenvolvimento de negócios, busco colocar minhas habilidades à disposição de uma organização inovadora, onde a excelência no atendimento e na negociação são fundamentais.</p>
                <p>Estou disponível para conversarmos sobre como posso agregar ao seu time com estratégias de crescimento rápido e eficaz. Vamos trabalhar juntos para aumentar a presença e a rentabilidade da sua empresa?</p>
                <a href="tel:+351965240987" class="cta-button">Falar Comigo</a>
            </div>
            <div class="footer">
                <p>Atenciosamente,<br>Ericlene De Sousa</p>
                <p><a href="mailto:ericlenedesousa@gmail.com">Contate-me por email</a></p>
            </div>
        </div>
    </body>
    </html>
    """
    msg.attach(MIMEText(body, 'html'))

    # Anexar o arquivo PDF do currículo
    filename = '/Users/programacao/Documents/binance_ai_trading_bot/curriculum/CV_Ericlene_Comercial.pdf'
    attachment = open(filename, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={filename}')
    msg.attach(part)

    # Enviar o email usando o Gmail SMTP
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_USER, to_email, msg.as_string())
        print(f'Email enviado para {to_email}')
        server.quit()
        registrar_email_enviado(to_email)  # Registrar o email como enviado
    except Exception as e:
        print(f'Erro ao enviar email: {e}')

# Função principal
def main():
    email_count = 0
    while True:  # Loop infinito para rodar o script indefinidamente
        with open('/Users/programacao/documents/binance_ai_trading_bot/job_hunter_netempregos/emails_extraidos.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                email_vaga = row[0].strip()  # Remover espaços em branco extras
                if email_vaga and email_vaga != 'email' and not verificar_email_enviado(email_vaga):  # Ignorar valores inválidos e já enviados
                    send_email(email_vaga)
                    email_count += 1
                    time.sleep(5)  # Delay de 5 segundos entre os envios (ajuste conforme necessário)
                
                if email_count >= 10:  # Limite de envios
                    print("Limite de envios atingido. Aguardando 30 segundos antes de continuar...")
                    break  # Pausa o envio e começa novamente o loop
        if email_count >= 10:
            time.sleep(30)  # Aguardar 30 segundos antes de continuar
            email_count = 0  # Resetar o contador para o próximo lote
        else:
            print("Nenhum novo email para enviar. Aguardando...") 
            time.sleep(60)  # Aguardar 1 minuto antes de verificar novamente

if __name__ == '__main__':
    main()
