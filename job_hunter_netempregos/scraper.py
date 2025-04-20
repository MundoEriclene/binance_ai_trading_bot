from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from config import CONFIG
from database import criar_csv_se_nao_existir, email_ja_enviado, registrar_email

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
    email.clear()
    senha.clear()
    email.send_keys(CONFIG["net_empregos_email"])
    senha.send_keys(CONFIG["net_empregos_password"])

    try:
        driver.switch_to.frame(driver.find_element(By.XPATH, "//iframe[contains(@src, 'recaptcha')]"))
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "recaptcha-anchor"))).click()
        driver.switch_to.default_content()
        print("[✓] reCAPTCHA clicado.")
        time.sleep(3)
    except:
        driver.switch_to.default_content()
        print("[•] CAPTCHA ignorado ou já validado.")

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "btnSubmit"))).click()
    print("[✓] Login enviado.")

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'Perfil')]"))
        )
        print("[✅] Login confirmado.")
    except:
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
    driver.get("https://www.net-empregos.com/index-candidato.asp")
    time.sleep(2)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "pesquisar"))).click()
    print("[✓] Clicou em PESQUISAR.")
    time.sleep(2)

    emails_extraidos = []
    pagina = 1

    while True:
        print(f"[→] Página {pagina}")
        fechar_anuncio_google(driver)
        time.sleep(2)

        divs_vagas = driver.find_elements(By.CSS_SELECTOR, "div.job-item.job-item-destaque.media")
        print(f"[•] {len(divs_vagas)} vagas encontradas.")

        for i in range(len(divs_vagas)):
            try:
                divs_vagas = driver.find_elements(By.CSS_SELECTOR, "div.job-item.job-item-destaque.media")
                a_tag = divs_vagas[i].find_element(By.CSS_SELECTOR, "a.oferta-link")
                href = a_tag.get_attribute("href")
                url_vaga = "https://www.net-empregos.com" + href if href.startswith("/") else href

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
                        time.sleep(2)
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

                driver.get("https://www.net-empregos.com/pesquisa-empregos.asp?page=" + str(pagina))
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "pesquisar"))
                )
                time.sleep(2)

            except Exception as e:
                print(f"[✗] Erro ao processar vaga: {e}")

        try:
            pagina += 1
            proximo = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.page-link.oferta-link.d-none.d-lg-block"))
            )
            driver.execute_script("arguments[0].click();", proximo)
            print("[→] Próxima página acessada com sucesso.\n")
            time.sleep(3)
        except Exception as e:
            print(f"[✗] Não encontrou botão de próxima página: {e}")
            print("[⚠️] Esperando 10 segundos antes de tentar novamente.")
            time.sleep(10)

    return emails_extraidos

def rodar_scraper():
    driver = iniciar_driver()
    try:
        fazer_login(driver)
        return buscar_emails_vagas(driver)
    finally:
        driver.quit()
