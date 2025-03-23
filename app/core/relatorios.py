import pandas as pd
from datetime import datetime, timedelta
from core.notificacoes import enviar_telegram

LOG_PATH = "logs/trades.log"

def carregar_trades():
    try:
        colunas = ["timestamp", "tipo", "preco", "quantidade", "lucro"]
        df = pd.read_csv(LOG_PATH, names=colunas)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        return df
    except Exception as e:
        print(f"Erro ao carregar log de trades: {e}")
        return pd.DataFrame()

def gerar_resumo(periodo="diario"):
    df = carregar_trades()
    if df.empty:
        return "Nenhuma operação registrada ainda."

    agora = datetime.utcnow()

    if periodo == "diario":
        inicio = agora.replace(hour=0, minute=0, second=0)
    elif periodo == "semanal":
        inicio = agora - timedelta(days=7)
    elif periodo == "mensal":
        inicio = agora - timedelta(days=30)
    else:
        return "Período inválido."

    df_periodo = df[df["timestamp"] >= inicio]

    total_trades = len(df_periodo[df_periodo["tipo"] == "venda"])
    lucro_total = df_periodo["lucro"].dropna().sum()

    resumo = f"""
📊 *Resumo {periodo.capitalize()} do RoboTrader*
--------------------------
🗓 Período: {inicio.date()} até {agora.date()}
💼 Total de vendas: {total_trades}
💰 Lucro acumulado: {lucro_total:.2f} USDT
"""

    return resumo

def enviar_resumo(periodo="diario"):
    resumo = gerar_resumo(periodo)
    enviar_telegram(resumo)
