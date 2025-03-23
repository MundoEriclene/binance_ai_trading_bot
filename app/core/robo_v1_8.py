import datetime
from core.binance_api import get_price, buy_crypto, sell_crypto
from core.notificacoes import enviar_telegram
from core.utils import calcular_rsi, registrar_trade

# === CONFIGURAÇÕES ===
SYMBOL = "BTCUSDT"
capital_usdt = 1000
score_minimo = 2
alvo_lucro_pct = 0.005  # 0.5%
estado = {"em_posicao": False, "preco_compra": 0.0, "btc_em_maos": 0.0, "data_entrada": None}

def executar_robo():
    preco = get_price(SYMBOL)
    if preco is None:
        return

    score = 0
    rsi = calcular_rsi(SYMBOL)

    if rsi and rsi < 35:
        score += 1
    # (Você pode adicionar mais critérios aqui como volume, tendência, etc)

    agora = datetime.datetime.utcnow()

    # === COMPRA ===
    if not estado["em_posicao"] and score >= score_minimo:
        quantidade_btc = capital_usdt / preco
        buy_crypto(SYMBOL, quantidade_btc)
        estado["em_posicao"] = True
        estado["preco_compra"] = preco
        estado["btc_em_maos"] = quantidade_btc
        estado["data_entrada"] = agora
        registrar_trade("compra", preco, quantidade_btc)
        enviar_telegram(f"✅ COMPRA realizada de {quantidade_btc:.5f} BTC a {preco:.2f} USDT")

    # === VENDA ===
    elif estado["em_posicao"]:
        preco_alvo = estado["preco_compra"] * (1 + alvo_lucro_pct)
        if preco >= preco_alvo:
            usdt_final = estado["btc_em_maos"] * preco
            sell_crypto(SYMBOL, estado["btc_em_maos"])
            lucro = usdt_final - capital_usdt
            registrar_trade("venda", preco, estado["btc_em_maos"], lucro)
            enviar_telegram(f"💰 VENDA executada por {preco:.2f} USDT | Lucro: {lucro:.2f} USDT")
            estado["em_posicao"] = False
            estado["btc_em_maos"] = 0.0
            estado["preco_compra"] = 0.0
            estado["data_entrada"] = None
