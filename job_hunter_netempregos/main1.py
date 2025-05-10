import time
import csv
import os
from email_sender1 import enviar_curriculo_teste

EMAILS_CSV = "emails_extraidos.csv"
EMAILS_ENVIADOS_CSV = "emails_enviados1.csv"

def ler_emails_arquivo(caminho):
    if not os.path.exists(caminho):
        return []
    with open(caminho, newline='', encoding='utf-8') as f:
        return [linha[0].strip().lower() for linha in csv.reader(f) if linha]

def salvar_email_enviado(email):
    with open(EMAILS_ENVIADOS_CSV, "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([email])

def main_loop():
    print("⏳ Iniciando robô de envio de currículos...")
    enviados = set(ler_emails_arquivo(EMAILS_ENVIADOS_CSV))

    while True:
        todos = ler_emails_arquivo(EMAILS_CSV)
        novos = [email for email in todos if email not in enviados]

        if not novos:
            print("🚫 Nenhum novo e-mail encontrado. Aguardando 15 segundos...")
            time.sleep(15)
            continue

        print(f"📨 {len(novos)} novos e-mails prontos para envio.")

        for i, email in enumerate(novos):
            try:
                print(f"➡️ Enviando currículo para: {email}")
                enviar_curriculo_teste(destinatario=email)
                salvar_email_enviado(email)
                enviados.add(email)
            except Exception as e:
                print(f"⚠️ Erro ao enviar para {email}: {e}")

            if (i + 1) % 10 == 0:
                print("⏱️ Aguardando 30 segundos após 10 envios...")
                time.sleep(30)

        print("✅ Ciclo concluído. Verificando por novos e-mails em breve...\n")
        time.sleep(10)

if __name__ == "__main__":
    main_loop()
