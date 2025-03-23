import time
from core.robo_v1_8 import executar_robo
from dotenv import load_dotenv
import os
from core.relatorios import enviar_resumo

# Enviar resumo a cada 24h (ex: via schedule)
enviar_resumo("diario")
enviar_resumo("semanal")
enviar_resumo("mensal")

# Carregar variáveis de ambiente
load_dotenv(dotenv_path='config/.env')

if __name__ == "__main__":
    print("🚀 RoboTrader V1.8 iniciado...")
    while True:
        try:
            executar_robo()
        except Exception as e:
            print(f"❌ Erro durante execução: {e}")
        time.sleep(5)  # espera 5 segundos
