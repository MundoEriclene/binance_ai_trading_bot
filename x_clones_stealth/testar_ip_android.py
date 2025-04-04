from playwright.sync_api import sync_playwright

def testar_ip_android():
    print("\n🌐 Iniciando navegador padrão (usando proxy do sistema)...\n")

    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=False)

        contexto = navegador.new_context()  # Sem proxy aqui

        pagina = contexto.new_page()

        try:
            pagina.goto("https://api.ipify.org/?format=json", timeout=15000)
            ip_publico = pagina.text_content("pre")
            print(f"✅ IP público detectado: {ip_publico}")
        except Exception as e:
            print(f"❌ Erro ao verificar IP: {e}")

        navegador.close()

if __name__ == "__main__":
    testar_ip_android()

