from scraper import rodar_scraper
from email_sender import enviar_email
from database import criar_csv_se_nao_existir, email_ja_enviado, registrar_email

def iniciar_envio():
    criar_csv_se_nao_existir()

    emails = rodar_scraper()
    if not emails:
        emails = []

    print(f"\n[✓] Total de e-mails encontrados: {len(emails)}\n")

    for email in emails:
        if email_ja_enviado(email):
            print(f"[!] E-mail já foi contactado anteriormente: {email}")
            continue

        sucesso = enviar_email(email)
        status = "Enviado" if sucesso else "Erro"
        registrar_email(email, status)

    print("\n✅ Processo concluído com sucesso.")

if __name__ == "__main__":
    iniciar_envio()
