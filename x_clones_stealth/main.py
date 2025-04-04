from playwright.sync_api import sync_playwright
import requests
import random
import string
import time
import re

MAIL_TM_API = "https://api.mail.tm"

def get_dominio_valido():
    res = requests.get(f"{MAIL_TM_API}/domains")
    dominios = res.json()["hydra:member"]
    if not dominios:
        raise Exception("❌ Nenhum domínio válido encontrado.")
    return dominios[0]["domain"]

def gerar_credenciais_mail_tm():
    dominio = get_dominio_valido()
    usuario = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    senha = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    email = f"{usuario}@{dominio}"

    print(f"📨 Criando email temporário: {email}")

    res = requests.post(f"{MAIL_TM_API}/accounts", json={"address": email, "password": senha})
    if res.status_code not in [200, 201]:
        raise Exception(f"❌ Erro ao criar conta Mail.tm: {res.text}")
    
    login = requests.post(f"{MAIL_TM_API}/token", json={"address": email, "password": senha})
    token = login.json()["token"]

    return email, senha, token

def aguardar_codigo(token, tempo_max=60):
    headers = {"Authorization": f"Bearer {token}"}
    print("⏳ Aguardando código do Facebook no email...")

    for _ in range(tempo_max):
        mensagens = requests.get(f"{MAIL_TM_API}/messages", headers=headers).json()
        if mensagens.get("hydra:member"):
            msg = mensagens["hydra:member"][0]
            msg_id = msg["id"]
            corpo = requests.get(f"{MAIL_TM_API}/messages/{msg_id}", headers=headers).json()["text"]
            match = re.search(r"FB-\d{5,6}", corpo)
            if match:
                return match.group(0)
        time.sleep(2)

    raise TimeoutError("⛔ Código do Facebook não chegou a tempo.")

def gerar_nome():
    nomes = ["Tiago", "João", "Pedro", "Lucas"]
    sobrenomes = ["Silva", "Sousa", "Oliveira", "Mendes"]
    return random.choice(nomes), random.choice(sobrenomes)

def preencher_lento(locator, texto, delay=5):
    locator.fill("")
    for char in texto:
        locator.type(char, delay=0.15)
    time.sleep(delay)

def salvar_em_txt(info):
    with open("contas_criadas.txt", "a") as f:
        f.write(info + "\n")

def criar_conta_facebook():
    email, senha_email, token = gerar_credenciais_mail_tm()

    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=False)
        contexto = navegador.new_context()
        pagina = contexto.new_page()

        print("🌍 Verificando IP...")
        pagina.goto("https://api.ipify.org/?format=json", timeout=15000)
        ip = pagina.text_content("body").replace("\n", "")
        print(f"✅ IP público detectado: {ip}")

        print("🌐 Acessando Facebook...")
        pagina.goto("https://www.facebook.com/reg", timeout=60000)
        time.sleep(5)

        print("✍️ Preenchendo formulário...")
        nome, sobrenome = gerar_nome()
        senha = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

        preencher_lento(pagina.locator("input[name='firstname']"), nome)
        preencher_lento(pagina.locator("input[name='lastname']"), sobrenome)
        preencher_lento(pagina.locator("input[name='reg_email__']"), email)

        campo_conf = pagina.locator("input[name='reg_email_confirmation__']")
        if campo_conf.is_visible():
            preencher_lento(campo_conf, email)
        preencher_lento(pagina.locator("input[name='reg_passwd__']"), senha)

        pagina.select_option("select[name='birthday_day']", "15")
        pagina.select_option("select[name='birthday_month']", "5")
        pagina.select_option("select[name='birthday_year']", "2000")
        pagina.locator("input[value='2']").check()

        print("📧 Email:", email)
        print("🔑 Senha:", senha)

        print("🚀 Clicando em 'Regista-te'...")
        botoes = pagina.locator("button[type='submit']")
        for i in range(botoes.count()):
            btn = botoes.nth(i)
            texto = btn.inner_text().strip().lower()
            elemento_pai = btn.evaluate("el => el.closest('#captcha_buttons')")
            if ("regista-te" in texto or "cadastre-se" in texto) and not elemento_pai:
                btn.click()
                break

        print("⏳ Aguardando redirecionamento...")
        time.sleep(10)

        status = "Falha"
        codigo = "Não recebido"
        try:
            codigo = aguardar_codigo(token)
            print(f"✅ Código do Facebook: {codigo}")
            pagina.fill("input[name='code']", codigo)

            continuar = pagina.locator("button:has-text('Continuar')")
            if continuar.is_visible():
                continuar.click()
                print("🎉 Conta criada com sucesso!")
                status = "Sucesso"
            else:
                print("⚠️ Botão 'Continuar' não visível.")
        except Exception as e:
            print(f"❌ Falha ao confirmar código: {e}")

        salvar_em_txt(f"{email} | {senha} | {ip} | {codigo} | {status}")
        input("🔒 Pressione [ENTER] para fechar o navegador...")
        navegador.close()

if __name__ == "__main__":
    criar_conta_facebook()
