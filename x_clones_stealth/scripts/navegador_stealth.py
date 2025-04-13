from playwright.sync_api import Browser, BrowserContext, Page

def criar_navegador(playwright) -> tuple[Browser, BrowserContext, Page]:
    """
    Cria um navegador Chromium com antidetecção e perfil natural.
    Retorna navegador, contexto e página.
    """
    navegador = playwright.chromium.launch(
        headless=False,
        args=[
            "--no-sandbox",
            "--disable-blink-features=AutomationControlled",
            "--disable-dev-shm-usage",
            "--disable-infobars",
            "--disable-gpu",
        ]
    )

    contexto = navegador.new_context(
        viewport={"width": 1280, "height": 720},
        locale="pt-PT",
        timezone_id="Europe/Lisbon",
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        geolocation={"latitude": 38.7169, "longitude": -9.1399},
        permissions=["geolocation"],
        is_mobile=False,
        device_scale_factor=1.0,
        has_touch=False
    )

    contexto.add_init_script(
        """
        // 🛡️ Anular fingerprints comuns
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        Object.defineProperty(navigator, 'languages', {get: () => ['pt-PT', 'pt']});
        Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
        window.navigator.chrome = { runtime: {} };
        window.console.debug = () => {};
        """
    )

    page = contexto.new_page()
    return navegador, contexto, page
