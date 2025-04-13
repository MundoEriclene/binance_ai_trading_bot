import asyncio
import random
import os
from playwright.async_api import async_playwright, TimeoutError
from pathlib import Path

CLONES_PATH = '../dados/clones_criados.txt'
LOG_PATH = '../logs/seguidores_log.txt'
COOKIE_DIR = '../cookies'
PAGINA_URL = 'https://www.facebook.com/share/1ANdVNJZ8t/'

async def preencher_lento(page, seletor, texto):
    campo = await page.wait_for_selector(seletor, timeout=15000)
    await campo.fill("")
    for letra in texto:
        await campo.type(letra, delay=0.12)
    await asyncio.sleep(1.2)

async def aceitar_cookie_se_existir(page):
    try:
        btn_xpath = '//span[contains(text(), "Permitir todos os cookies")]'
        await page.wait_for_selector(f'xpath={btn_xpath}', timeout=10000)
        await page.click(f'xpath={btn_xpath}')
        print("[🍪] Cookies aceitos com sucesso.")
        await asyncio.sleep(2)
    except TimeoutError:
        print("[ℹ️] Nenhum botão de cookies encontrado.")

async def login_necessario(page):
    try:
        await page.wait_for_selector('input[name="email"]', timeout=8000)
        return True
    except:
        return False

async def login_e_seguir(p, email, senha):
    print(f"[🌀] Iniciando sessão com: {email}")

    user_folder = os.path.join(COOKIE_DIR, email.split('@')[0])
    context = await p.chromium.launch_persistent_context(
        user_data_dir=user_folder,
        headless=False,
        permissions=[],
        viewport={"width": 1280, "height": 720},
        args=["--disable-notifications"]
    )

    page = await context.new_page()
    await page.goto("https://facebook.com", timeout=60000)
    await aceitar_cookie_se_existir(page)

    precisa_login = await login_necessario(page)

    if precisa_login:
        try:
            await preencher_lento(page, 'input[name="email"]', email.strip())
            await preencher_lento(page, 'input[name="pass"]', senha.strip())
            await page.click('button[name="login"]')
            await page.wait_for_timeout(5000)

            if "login" in page.url:
                print(f"[❌] Login falhou para {email}")
                await context.close()
                return False
            print(f"[✅] Login bem-sucedido: {email}")
        except Exception as e:
            print(f"[💥] Erro durante login de {email}: {e}")
            await context.close()
            return False
    else:
        print(f"[🔓] Já logado como {email}")

    await page.goto(PAGINA_URL)
    await page.wait_for_timeout(random.randint(3000, 6000))

    try:
        # Captura qualquer botão que contenha "Seguir" ou "A seguir"
        btn_xpath = '//span[contains(text(), "Seguir") or contains(text(), "A seguir")]'
        await page.wait_for_selector(f'xpath={btn_xpath}', timeout=10000)
        btn_element = await page.query_selector(f'xpath={btn_xpath}')
        texto = (await btn_element.inner_text()).strip().lower()

        if texto == "seguir":
            await btn_element.click()
            await page.wait_for_timeout(2000)
            print(f"[🎯] Página seguida com sucesso: {email}")
            with open(LOG_PATH, 'a') as log:
                log.write(f"{email} | Seguiu agora\n")
        else:
            print(f"[✔️] Já estava seguindo: {email}")
            with open(LOG_PATH, 'a') as log:
                log.write(f"{email} | Já seguia\n")

    except TimeoutError:
        print(f"[⚠️] Botão de seguir não encontrado para {email}")

    await context.close()

async def main():
    Path(COOKIE_DIR).mkdir(parents=True, exist_ok=True)
    Path('../logs').mkdir(parents=True, exist_ok=True)

    with open(CLONES_PATH, 'r') as f:
        linhas = f.readlines()

    for linha in linhas:
        partes = linha.split('|')
        if len(partes) < 2:
            continue

        email = partes[0].strip()
        senha = partes[1].strip()

        async with async_playwright() as p:
            await login_e_seguir(p, email, senha)

        await asyncio.sleep(random.randint(8, 15))

if __name__ == "__main__":
    asyncio.run(main())
