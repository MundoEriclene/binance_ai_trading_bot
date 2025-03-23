import pandas as pd
import matplotlib.pyplot as plt
from ta.momentum import RSIIndicator

# === CONFIGURAÇÕES ===
capital_inicial = 1000
lucro_desejado = 0.02  # 2% de lucro alvo
arquivo_csv = '../data/processed/btc_usdt_m5.csv'

# === CARREGAR DADOS ===
df = pd.read_csv(arquivo_csv, parse_dates=['timestamp'])
df.set_index('timestamp', inplace=True)
df['close'] = df['close'].astype(float)

# === CALCULAR RSI ===
rsi = RSIIndicator(close=df['close'], window=14)
df['RSI'] = rsi.rsi()

# === VARIÁVEIS DE CONTROLE ===
em_posicao = False
preco_compra = 0
capital = capital_inicial
btc_em_maos = 0
preco_alvo = 0
data_entrada = None
historico = []

# === LOOP DO BACKTEST ===
for i in range(len(df)):
    preco = df['close'].iloc[i]
    rsi_valor = df['RSI'].iloc[i]
    timestamp = df.index[i]

    # Lógica de compra
    if not em_posicao and rsi_valor < 30:
        btc_em_maos = capital / preco
        preco_compra = preco
        preco_alvo = preco_compra * (1 + lucro_desejado)
        data_entrada = timestamp
        em_posicao = True

        historico.append({
            'ação': 'compra',
            'timestamp': timestamp,
            'preço': preco,
            'btc': btc_em_maos
        })

    # Lógica de venda via LIMIT
    elif em_posicao and preco >= preco_alvo:
        capital = btc_em_maos * preco
        lucro_pct = (preco - preco_compra) / preco_compra * 100
        tempo_espera = (timestamp - data_entrada).total_seconds() / 3600  # em horas

        historico.append({
            'ação': 'venda',
            'timestamp': timestamp,
            'preço': preco,
            'lucro_%': round(lucro_pct, 2),
            'capital_atual': round(capital, 2),
            'tempo_espera_h': round(tempo_espera, 2)
        })

        em_posicao = False
        btc_em_maos = 0
        preco_compra = 0
        preco_alvo = 0
        data_entrada = None

# === RESULTADOS ===
historico_df = pd.DataFrame(historico)
historico_df.to_csv('../data/processed/backtest_resultado_v1_1.csv', index=False)

lucro_total = ((capital - capital_inicial) / capital_inicial) * 100
total_trades = len(historico_df) // 2
tempo_medio = historico_df[historico_df['ação'] == 'venda']['tempo_espera_h'].mean()

print(f"\n📈 Backtest finalizado - RoboTrader V1.1 (LIMIT)")
print(f"💰 Lucro total: {lucro_total:.2f}%")
print(f"📊 Total de operações: {total_trades} trades")
print(f"⏱ Tempo médio por operação: {tempo_medio:.2f} horas\n")

# === GRÁFICO ===
plt.figure(figsize=(14,6))
plt.plot(df['close'], label='Preço BTC/USDT', alpha=0.5)

compras = historico_df[historico_df['ação'] == 'compra']
vendas = historico_df[historico_df['ação'] == 'venda']

plt.scatter(compras['timestamp'], compras['preço'], marker='^', color='green', label='Compra', s=50)
plt.scatter(vendas['timestamp'], vendas['preço'], marker='v', color='red', label='Venda', s=50)

plt.title('RoboTrader V1.1 - Estratégia RSI + Venda LIMIT (BTC/USDT - M5)')
plt.xlabel('Data')
plt.ylabel('Preço (USDT)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
