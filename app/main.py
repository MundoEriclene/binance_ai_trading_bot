import threading
import time
import schedule
from core.robo_v1_8 import executar_robo
from core.relatorios import enviar_resumo
from core.notificacoes import enviar_telegram
from dotenv import load_dotenv
from fake_server import app

load_dotenv(dotenv_path='config/.env')

# Iniciar robô
def iniciar_robo():
    enviar_telegram("🚀 RoboTrader V1.8 (modo grátis) está ONLINE na nuvem!")
    while True:
        try:
            executar_robo()
        except Exception as e:
            erro = f"❌ ERRO no robô:\n{str(e)}"
            print(erro)
            enviar_telegram(erro)
        schedule.run_pending()
        time.sleep(5)

# Agendar relatórios
schedule.every().day.at("23:59").do(lambda: enviar_resumo("diario"))
schedule.every().monday.at("09:00").do(lambda: enviar_resumo("semanal"))
schedule.every().day.at("00:05").do(lambda: enviar_resumo("mensal"))

if __name__ == "__main__":
    threading.Thread(target=iniciar_robo).start()
    app.run(host="0.0.0.0", port=10000)
