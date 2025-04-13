import sys
import os
import time
import random
import string
import re
import imaplib
import email
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scripts.trocar_ip import trocar_ip_android
from scripts.navegador_stealth import criar_navegador
from scripts.gerar_email import gerar_email
from scripts.salvar_conta import salvar_conta
from scripts.nome_aleatorio import gerar_nome_unico
from scripts.verificar_existencia import email_ja_usado

# 🔐 Variáveis de ambiente
load_dotenv("/Users/programacao/Documents/binance_ai_trading_bot/config/.env")
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")

# ⚙️ Configurações
PELOTAO_ID = 1
TOTAL_CONTAS = 10000


def aguardar_codigo(destinatario, tempo_max=60):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(GMAIL_USER, GMAIL_PASSWORD)

    for tentativa in range(tempo_max):
        mail.select("inbox")
        result, data = mail.search(None, 'ALL')
        for num in data[0].split()[::-1]:
            result, msg_data = mail.fetch(num, '(RFC822)')
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            if msg["To"] and destinatario in msg["To"]:
                corpo = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            corpo += part.get_payload(decode=True).decode(errors="ignore")
                else:
                    corpo = msg.get_payload(decode=True).decode(errors="ignore")

                match = re.search(r"FB[- ]?(\d{5,6})", corpo)
                if match:
                    return match.group(1)

        print(f"[📨] Tentativa {tentativa + 1}/{tempo_max} para buscar código...")
        time.sleep(1)

    return None


def preencher_humano(page, seletor, texto):
    campo = page.locator(seletor)
    campo.scroll_into_view_if_needed()
    campo.wait_for()
    campo.click()
    campo.fill("")
    for letra in texto:
        campo.type(letra, delay=random.uniform(0.08, 0.25))
    time.sleep(random.uniform(0.5, 1.2))


def criar_clone_facebook():
    trocar_ip_android()
    email_clone = gerar_email()
    if email_ja_usado(PELOTAO_ID, email_clone):
        print(f"[⏩] Email {email_clone} já usado. Pulando...")
        return

    nome, sobrenome = gerar_nome_unico()
    senha = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    status = "❌ Falhou"

    with sync_playwright() as p:
        navegador, contexto, page = criar_navegador(p)
        page.goto("https://facebook.com/reg", timeout=60000)
        time.sleep(2.5)

        # ✅ Cookies
        try:
            page.wait_for_timeout(2000)
            cookies_span = page.locator("//span[contains(text(), 'Permitir todos os cookies')]").first
            cookies_span.click(force=True)
            print("[🍪] Cookies aceitos com clique forçado.")
            time.sleep(1.5)
        except Exception as e:
            print(f"[⚠️] Cookies não exibidos: {e}")

        # ✅ Preenchendo formulário
        preencher_humano(page, 'input[name="firstname"]', nome)
        preencher_humano(page, 'input[name="lastname"]', sobrenome)
        preencher_humano(page, 'input[name="reg_email__"]', email_clone)
        time.sleep(1.2)

        if page.locator('input[name="reg_email_confirmation__"]').is_visible():
            preencher_humano(page, 'input[name="reg_email_confirmation__"]', email_clone)

        preencher_humano(page, 'input[name="reg_passwd__"]', senha)

        page.select_option('select[name="birthday_day"]', str(random.randint(1, 28)))
        time.sleep(0.5)
        page.select_option('select[name="birthday_month"]', str(random.randint(1, 12)))
        time.sleep(0.5)
        page.select_option('select[name="birthday_year"]', str(random.randint(1980, 2003)))
        time.sleep(0.5)

        sexo_radio = page.locator('input[value="2"]')
        sexo_radio.scroll_into_view_if_needed()
        sexo_radio.click()
        time.sleep(1.2)

        # ✅ Submete o formulário
        botoes = page.locator("button[type='submit']")
        for i in range(botoes.count()):
            btn = botoes.nth(i)
            texto = btn.inner_text().strip().lower()
            if "regista" in texto or "cadastre" in texto:
                btn.scroll_into_view_if_needed()
                btn.click()
                break

        time.sleep(6)
        codigo = aguardar_codigo(email_clone)

        if codigo:
            print(f"[🔐] Código recebido: {codigo}")
            preencher_humano(page, 'input[name="code"]', codigo)
            continuar_btn = page.locator('button:has-text("Continuar")')
            if continuar_btn.is_visible():
                continuar_btn.scroll_into_view_if_needed()
                continuar_btn.click()
                status = "✅ Sucesso"
        else:
            print("[⛔] Código não recebido.")

        salvar_conta(PELOTAO_ID, email_clone, senha, nome, sobrenome, status, codigo)

        # ✅ Salvar estado do navegador
        pasta_estado = f"../pelotoes/pelotao_{PELOTAO_ID}"
        os.makedirs(pasta_estado, exist_ok=True)
        contexto.storage_state(path=os.path.join(pasta_estado, f"estado_{email_clone}.json"))

        navegador.close()


if __name__ == "__main__":
    contas_criadas = 0
    while contas_criadas < TOTAL_CONTAS:
        try:
            criar_clone_facebook()
            contas_criadas += 1
        except Exception as e:
            print(f"[💥] Erro inesperado: {e}")
            continue
