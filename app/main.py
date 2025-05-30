import threading
import time
import schedule
import datetime
from core.robo_v1_8 import executar_robo
from core.notificacoes import enviar_telegram
from core.relatorios import enviar_relatorio
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

# ✅ Verifica se é o 1º dia do mês
def verificar_envio_mensal():
    hoje = datetime.datetime.utcnow()
    if hoje.day == 1:
        enviar_relatorio("Mensal")

# Agendar relatórios
schedule.every().day.at("23:59").do(lambda: enviar_relatorio("Diário"))
schedule.every().friday.at("23:59").do(lambda: enviar_relatorio("Semanal"))
schedule.every().day.at("01:00").do(verificar_envio_mensal)  # ⬅️ Corrigido

if __name__ == "__main__":
    threading.Thread(target=iniciar_robo).start()
    app.run(host="0.0.0.0", port=10000)
