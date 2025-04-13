import asyncio
import random
import os
from pathlib import Path
from playwright.async_api import async_playwright

CLONES_PATH = '../dados/clones_criados.txt'
LOG_PATH = '../logs/comentarios_log.txt'
COOKIE_DIR = '../cookies'

URLS = [
    "https://www.facebook.com/reel/914203170804829",
    "https://www.facebook.com/photo?fbid=200243748718000&set=a.106024458139930"
]

comentarios_reels = [
    "Esse áudio é real demais 😂🔥",
    "Quando o Bitcoin bate 100k eu mando igual",
    "Kkkkk esse é o espírito 😎",
    "Só os insiders sabem pra onde vão 💰",
    "Ghost-1970 já avisou..."
]

comentarios_fotos = [
    "Lei da Atração é real! 🔥",
    "A mente é o ativo mais poderoso 🧠",
    "Visual incrível com mensagem profunda!",
    "Ghost-1970 tá moldando o mundo.",
    "Quem pensa grande atrai grandeza 💎"
]

async def login_necessario(page):
    try:
        await page.wait_for_selector('input[name="email"]', timeout=8000)
        return True
    except:
        return False

async def comentar_reel(page):
    try:
        await page.wait_for_selector('div[aria-label="Comentar"]', timeout=8000)
        await page.click('div[aria-label="Comentar"]')
        await asyncio.sleep(2)

        campo = await page.wait_for_selector('div[contenteditable="true"]', timeout=5000)
        comentario = random.choice(comentarios_reels)
        await campo.click()
        await campo.type(comentario, delay=60)
        await asyncio.sleep(1)
        await page.keyboard.press("Enter")
        print(f"[🎬] Comentou no REEL: {comentario}")
        return comentario
    except Exception as e:
        print(f"[⚠️] Falha ao comentar no REEL: {e}")
        return None

async def curtir_reel(page):
    try:
        botao_like = await page.query_selector('div[aria-label="Gosto"]')
        if botao_like:
            await botao_like.click()
            print("[❤️] Reel curtido com sucesso.")
    except:
        print("[⚠️] Não foi possível curtir o Reel.")

async def comentar_foto(page):
    try:
        await page.wait_for_selector('div[contenteditable="true"]', timeout=8000)
        campo = await page.query_selector('div[contenteditable="true"]')
        comentario = random.choice(comentarios_fotos)
        await campo.click()
        await campo.type(comentario, delay=60)
        await asyncio.sleep(1)
        await page.keyboard.press("Enter")
        print(f"[🖼️] Comentou na FOTO: {comentario}")
        return comentario
    except Exception as e:
        print(f"[⚠️] Falha ao comentar na FOTO: {e}")
        return None


async def curtir_foto(page):
    try:
        btn = await page.query_selector('div[aria-label="Gosto"]')
        if btn:
            await btn.click()
            print("[👍] Curtida na foto enviada.")
    except:
        print("[⚠️] Não foi possível curtir a foto.")

async def comentar_url(p, email, senha, url):
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

    if await login_necessario(page):
        await page.fill('input[name="email"]', email)
        await page.fill('input[name="pass"]', senha)
        await page.click('button[name="login"]')
        await page.wait_for_timeout(5000)

    await page.goto(url)
    await page.wait_for_timeout(5000)

    comentario = None
    if "reel" in url:
        comentario = await comentar_reel(page)
        await curtir_reel(page)
    elif "photo" in url:
        comentario = await comentar_foto(page)
        await curtir_foto(page)
    else:
        print("[⚠️] URL não reconhecida.")

    if comentario:
        with open(LOG_PATH, "a") as f:
            f.write(f"{email} | {url} | Comentário: {comentario}\n")

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
            for url in URLS:
                await comentar_url(p, email, senha, url)
                await asyncio.sleep(random.randint(8, 15))

if __name__ == "__main__":
    asyncio.run(main())
