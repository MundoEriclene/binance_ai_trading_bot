import csv
import os

CAMINHO_CSV = "emails_extraidos.csv"

def criar_csv_se_nao_existir():
    if not os.path.exists(CAMINHO_CSV):
        with open(CAMINHO_CSV, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["email", "status"])

def email_ja_enviado(email):
    if not os.path.exists(CAMINHO_CSV):
        return False
    with open(CAMINHO_CSV, newline="") as f:
        reader = csv.DictReader(f)
        return any(row["email"] == email for row in reader)

def registrar_email(email, status="Extraído"):
    with open(CAMINHO_CSV, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([email, status])
