import pandas as pd
import matplotlib.pyplot as plt
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator

# === CONFIGURAÇÕES ===
capital_inicial = 1000
arquivo_csv = '../data/processed/btc_usdt_m5.csv'
SCORE_MINIMO = 2
ALVO_LUCRO_FIXO = 0.005  # 0.5%

# === CARREGAR DADOS ===
df = pd.read_csv(arquivo_csv, parse_dates=['timestamp'])
df.set_index('timestamp', inplace=True)
df['close'] = df['close'].astype(float)
df['open'] = df['open'].astype(float)
df['volume'] = df['volume'].astype(float)
df['high'] = df['high'].astype(float)
df['low'] = df['low'].astype(float)

# === INDICADORES ===
df['RSI'] = RSIIndicator(close=df['close'], window=14).rsi()
df['EMA20'] = EMAIndicator(close=df['close'], window=20).ema_indicator()
df['EMA50'] = EMAIndicator(close=df['close'], window=50).ema_indicator()
df['vol_media'] = df['volume'].rolling(window=20).mean()

# === VARIÁVEIS ===
capital = capital_inicial
em_posicao = False
preco_compra = 0
btc_em_maos = 0
data_entrada = None
historico = []

# === BACKTEST ===
for i in range(1, len(df)):
    preco = df['close'].iloc[i]
    rsi = df['RSI'].iloc[i]
    ema20 = df['EMA20'].iloc[i]
    ema50 = df['EMA50'].iloc[i]
    volume = df['volume'].iloc[i]
    vol_media = df['vol_media'].iloc[i]
    open_candle = df['open'].iloc[i]
    close_anterior = df['close'].iloc[i - 1]
    timestamp = df.index[i]

    # === SCORE SYSTEM ===
    score = 0
    if rsi < 35:
        score += 1
    if volume > vol_media:
        score += 1
    if preco > open_candle and preco > close_anterior:
        score += 1
    if ema20 > ema50:
        score += 1

    # === COMPRA ===
    if not em_posicao and score >= SCORE_MINIMO:
        preco_compra = preco
        btc_em_maos = capital / preco
        data_entrada = timestamp
        em_posicao = True
        historico.append({
            'ação': 'compra',
            'timestamp': timestamp,
            'preço': preco,
            'btc': btc_em_maos,
            'score_entrada': score
        })

    # === VENDA ===
    elif em_posicao:
        preco_alvo = preco_compra * (1 + ALVO_LUCRO_FIXO)
        if preco >= preco_alvo:
            capital = btc_em_maos * preco
            lucro_pct = (preco - preco_compra) / preco_compra * 100
            tempo_espera = (timestamp - data_entrada).total_seconds() / 3600
            historico.append({
                'ação': 'venda',
                'timestamp': timestamp,
                'preço': preco,
                'lucro_%': round(lucro_pct, 2),
                'capital_atual': round(capital, 2),
                'tempo_espera_h': round(tempo_espera, 2),
                'alvo_atingido': f"{int(ALVO_LUCRO_FIXO*100)}%"
            })
            em_posicao = False
            preco_compra = 0
            btc_em_maos = 0
            data_entrada = None

# === RESULTADOS ===
historico_df = pd.DataFrame(historico)
historico_df.to_csv('../data/processed/backtest_resultado_v1_8.csv', index=False)

trades_feitos = len(historico_df[historico_df['ação'] == 'venda'])
lucro_total = ((capital - capital_inicial) / capital_inicial) * 100
tempo_medio = historico_df[historico_df['ação'] == 'venda']['tempo_espera_h'].mean()

print(f"\n🤖 RoboTrader V1.8 - Backtest Finalizado (1 Ordem por vez)")
print(f"💰 Lucro total: {lucro_total:.2f}%")
print(f"📊 Total de trades: {trades_feitos}")
print(f"⏱ Tempo médio por operação: {tempo_medio:.2f} horas\n")

# === GRÁFICO ===
plt.figure(figsize=(14,6))
plt.plot(df['close'], label='Preço BTC/USDT', alpha=0.5)

compras = historico_df[historico_df['ação'] == 'compra']
vendas = historico_df[historico_df['ação'] == 'venda']

plt.scatter(compras['timestamp'], compras['preço'], marker='^', color='green', label='Compra', s=60)
plt.scatter(vendas['timestamp'], vendas['preço'], marker='v', color='red', label='Venda', s=60)

plt.title('RoboTrader V1.8 - 1 Ordem por vez (BTC/USDT - M5)')
plt.xlabel('Data')
plt.ylabel('Preço (USDT)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
