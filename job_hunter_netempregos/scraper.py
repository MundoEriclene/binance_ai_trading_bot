from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from config import CONFIG
from database import criar_csv_se_nao_existir, email_ja_enviado, registrar_email

CAMINHO_PAGINA = "ultima_pagina.txt"

def salvar_pagina_atual(pagina):
    with open(CAMINHO_PAGINA, "w") as f:
        f.write(str(pagina))

def carregar_pagina_inicial():
    try:
        with open(CAMINHO_PAGINA, "r") as f:
            return int(f.read().strip())
    except:
        return 1

def iniciar_driver(manter_aberto=False):
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    if manter_aberto:
        options.add_experimental_option("detach", True)
    return webdriver.Chrome(options=options)

def fechar_anuncio_google(driver):
    try:
        WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Fechar']"))
        ).click()
        print("[✓] Anúncio Google fechado.")
        time.sleep(1)
    except:
        pass

def aguardar_resolucao_captcha(driver):
    print("[⏳] Aguardando você resolver o CAPTCHA manualmente... (sem limite de tempo)")
    driver.switch_to.default_content()
    while True:
        try:
            driver.switch_to.frame(driver.find_element(By.XPATH, "//iframe[contains(@src, 'recaptcha')]"))
            checkbox = driver.find_element(By.ID, "recaptcha-anchor")
            if "recaptcha-checkbox-checked" in checkbox.get_attribute("class"):
                print("[✓] CAPTCHA resolvido manualmente.")
                driver.switch_to.default_content()
                return True
        except:
            pass
        driver.switch_to.default_content()
        print("[⏳] Ainda aguardando você resolver o CAPTCHA manualmente...")
        time.sleep(3)

def esta_logado(driver):
    try:
        driver.find_element(By.XPATH, "//a[contains(text(),'Perfil')]")
        return True
    except:
        return False

def fazer_login(driver):
    print("[•] Realizando login completo...")
    driver.get("https://www.net-empregos.com/loginc.asp")
    time.sleep(2)

    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Permitir todos')]"))
        ).click()
        print("[✓] Cookies aceitos.")
    except:
        print("[•] Sem popup de cookies.")

    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Não Ativar')]"))
        ).click()
        print("[✓] Alerta fechado.")
    except:
        print("[•] Sem alerta visível.")

    email = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "user")))
    senha = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "pwd")))
    email.clear(); senha.clear()
    email.send_keys(CONFIG["net_empregos_email"])
    senha.send_keys(CONFIG["net_empregos_password"])

    try:
        driver.switch_to.frame(driver.find_element(By.XPATH, "//iframe[contains(@src, 'recaptcha')]"))
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "recaptcha-anchor"))).click()
        driver.switch_to.default_content()
        aguardar_resolucao_captcha(driver)
    except:
        driver.switch_to.default_content()
        print("[•] CAPTCHA ignorado ou já validado.")

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "btnSubmit"))).click()
    print("[✓] Login enviado.")

    if esta_logado(driver):
        print("[✅] Login confirmado.")
    else:
        print("[✗] Login falhou ou não foi redirecionado.")

def login_modal(driver):
    try:
        modal = driver.find_element(By.ID, "frmReminder")
        if modal.is_displayed():
            print("[⚠️] Modal de login visível.")
            campo_email = modal.find_element(By.ID, "mail")
            campo_email.clear()
            campo_email.send_keys(CONFIG["net_empregos_email"])
            modal.find_element(By.ID, "btnReminder").click()
            time.sleep(3)
            if "/loginc.asp" in driver.current_url:
                fazer_login(driver)
                return True
    except:
        pass
    return False

def buscar_emails_vagas(driver):
    criar_csv_se_nao_existir()
    pagina = carregar_pagina_inicial()

    driver.get("https://www.net-empregos.com/index-candidato.asp")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "pesquisar"))).click()
    print("[✓] Clicou em PESQUISAR.")
    time.sleep(2)

    emails_extraidos = []

    while True:
        print(f"[→] Página {pagina}")
        salvar_pagina_atual(pagina)
        driver.get(f"https://www.net-empregos.com/pesquisa-empregos.asp?page={pagina}")
        time.sleep(2)
        fechar_anuncio_google(driver)

        if not esta_logado(driver):
            print("[✗] Sessão parece ter expirado. Reautenticando...")
            fazer_login(driver)
            continue

        vagas = driver.find_elements(By.CSS_SELECTOR, "div.job-item.media")  # pega todas as divs, mesmo fora do destaque
        print(f"[•] {len(vagas)} vagas encontradas.")

        if not vagas:
            print("[✗] Nenhuma vaga visível na estrutura da página.")
            pagina += 1
            salvar_pagina_atual(pagina)
            continue

        links_vagas = []
        for div in vagas:
            try:
                a_tag = div.find_element(By.CSS_SELECTOR, "a.oferta-link")
                href = a_tag.get_attribute("href")
                if href:
                    links_vagas.append("https://www.net-empregos.com" + href if href.startswith("/") else href)
            except Exception as e:
                print(f"[✗] Erro ao extrair link de vaga: {e}")

        for url_vaga in links_vagas:
            try:
                driver.get(url_vaga)
                time.sleep(2)
                fechar_anuncio_google(driver)

                try:
                    WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "job-mail"))
                    ).click()
                    time.sleep(1)
                    if login_modal(driver):
                        driver.get(url_vaga)
                        WebDriverWait(driver, 3).until(
                            EC.element_to_be_clickable((By.CLASS_NAME, "job-mail"))
                        ).click()
                        time.sleep(1)
                except:
                    print("[•] Sem botão 'Mostrar Email'.")

                try:
                    email_element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, "//a[starts-with(@href,'mailto:')]"))
                    )
                    email = email_element.get_attribute("href").replace("mailto:", "").split("?")[0]
                    if email_ja_enviado(email):
                        print(f"[•] Já registrado: {email}")
                    else:
                        registrar_email(email, "Extraído")
                        emails_extraidos.append(email)
                        print(f"[+] Email salvo: {email}")
                except:
                    print("[!] E-mail não encontrado.")

            except Exception as e:
                print(f"[✗] Erro ao processar vaga: {e}")

        pagina += 1
        salvar_pagina_atual(pagina)

    return emails_extraidos

def rodar_scraper():
    driver = iniciar_driver()
    try:
        fazer_login(driver)
        return buscar_emails_vagas(driver)
    finally:
        driver.quit()
