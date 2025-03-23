import datetime
from core.binance_api import get_price, buy_crypto, sell_crypto
from core.utils import calcular_rsi, registrar_trade
from core.notificacoes import enviar_telegram, reportar_erro
import json
import os
from datetime import datetime

def salvar_log(tipo, **kwargs):
    log_path = "core/logs/log_diario.json"
    if not os.path.exists("core/logs"):
        os.makedirs("core/logs")
    log = []
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            log = json.load(f)
    registro = {"tipo": tipo, "timestamp": str(datetime.utcnow())}
    registro.update(kwargs)
    log.append(registro)
    with open(log_path, "w") as f:
        json.dump(log, f, indent=2)

# === CONFIGURAÇÕES ===
SYMBOL = "BTCUSDT"
capital_usdt = 1000
score_minimo = 2
alvo_lucro_pct = 0.005  # 0.5%
estado = {"em_posicao": False, "preco_compra": 0.0, "btc_em_maos": 0.0, "data_entrada": None}

def executar_robo():
    try:
        preco = get_price(SYMBOL)
        if preco is None:
            return

        score = 0
        rsi = calcular_rsi(SYMBOL)
        if rsi and rsi < 35:
            score += 1

        agora = datetime.utcnow()

        # === COMPRA ===
        if not estado["em_posicao"] and score >= score_minimo:
            quantidade_btc = capital_usdt / preco
            buy_crypto(SYMBOL, quantidade_btc)
            estado["em_posicao"] = True
            estado["preco_compra"] = preco
            estado["btc_em_maos"] = quantidade_btc
            estado["data_entrada"] = agora
            registrar_trade("compra", preco, quantidade_btc)

            salvar_log("compra", preco=preco)

            mensagem = f"""✅ *COMPRA REALIZADA*
🕒 {agora}
💰 Preço: {preco:.2f}
📊 SCORE: {score}/4
📈 Ativo: {SYMBOL}"""
            enviar_telegram(mensagem)

        # === VENDA ===
        elif estado["em_posicao"]:
            preco_alvo = estado["preco_compra"] * (1 + alvo_lucro_pct)
            if preco >= preco_alvo:
                usdt_final = estado["btc_em_maos"] * preco
                lucro = usdt_final - capital_usdt
                tempo_espera = (agora - estado["data_entrada"]).total_seconds() / 3600

                sell_crypto(SYMBOL, estado["btc_em_maos"])
                registrar_trade("venda", preco, estado["btc_em_maos"], lucro)

                salvar_log("venda", preco=preco, lucro=lucro)

                mensagem = f"""💸 *VENDA EXECUTADA*
🕒 {agora}
💰 Venda a: {preco:.2f}
📈 Lucro: {lucro:.2f} USDT
⏱ Espera: {tempo_espera:.2f}h
📈 Ativo: {SYMBOL}"""
                enviar_telegram(mensagem)

                estado["em_posicao"] = False
                estado["btc_em_maos"] = 0.0
                estado["preco_compra"] = 0.0
                estado["data_entrada"] = None

        # === LOG DE MONITORAMENTO ===
        else:
            enviar_telegram(f"⏳ Aguardando oportunidade... SCORE atual: {score}/4")

    except Exception as e:
        mensagem = str(e)
        salvar_log("erro", mensagem=mensagem)
        reportar_erro(mensagem)
