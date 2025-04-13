from playwright.sync_api import sync_playwright

def abrir_navegador_manual():
    with sync_playwright() as p:
        navegador = p.chromium.launch(
            headless=False,
            args=[
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
            ]
        )

        contexto = navegador.new_context(
            viewport={"width": 1280, "height": 720},
            locale="pt-PT",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        )

        contexto.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            window.navigator.chrome = { runtime: {} };
            Object.defineProperty(navigator, 'languages', {get: () => ['pt-PT', 'pt']});
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]});
        """)

        page = contexto.new_page()
        page.goto("https://facebook.com", timeout=60000)

        print("🌐 Navegador aberto! Agora você pode tentar criar uma conta manualmente.")
        print("⚠️ Verifique se há CAPTCHA, erros ou comportamentos diferentes.")
        input("⏹ Pressione ENTER para fechar...")
        navegador.close()

if __name__ == "__main__":
    abrir_navegador_manual()
