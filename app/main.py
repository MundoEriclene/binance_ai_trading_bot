import time
import schedule
from core.robo_v1_8 import executar_robo
from core.relatorios import enviar_resumo
from dotenv import load_dotenv

load_dotenv(dotenv_path='config/.env')

# Agendar relatórios
schedule.every().day.at("23:59").do(lambda: enviar_resumo("diario"))
schedule.every().monday.at("09:00").do(lambda: enviar_resumo("semanal"))
schedule.every().day.at("00:05").do(lambda: enviar_resumo("mensal"))

if __name__ == "__main__":
    print("🚀 RoboTrader V1.8 iniciado...")
    while True:
        try:
            executar_robo()
        except Exception as e:
            from core.notificacoes import enviar_telegram
            enviar_telegram(f"❌ ERRO no robô: {str(e)}")
            print(f"❌ Erro: {e}")
        
        schedule.run_pending()
        time.sleep(5)
