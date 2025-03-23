import pandas as pd
import matplotlib.pyplot as plt
from ta.momentum import RSIIndicator

# === CONFIGURAÇÕES ===
capital_inicial = 1000
spread = 0.012  # 1.2% (simula o CONVERTER da Binance)
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
historico = []

# === LOOP DO BACKTEST ===
for i in range(len(df)):
    preco = df['close'].iloc[i]
    rsi_valor = df['RSI'].iloc[i]
    timestamp = df.index[i]

    if not em_posicao and rsi_valor < 30:
        btc_em_maos = capital / preco
        preco_compra = preco
        em_posicao = True
        historico.append({
            'ação': 'compra',
            'timestamp': timestamp,
            'preço': preco,
            'btc': btc_em_maos
        })

    elif em_posicao:
        preco_venda_liquido = preco * (1 - spread)
        if preco_venda_liquido > preco_compra:
            capital = btc_em_maos * preco_venda_liquido
            lucro_pct = (preco_venda_liquido - preco_compra) / preco_compra * 100
            historico.append({
                'ação': 'venda',
                'timestamp': timestamp,
                'preço': preco,
                'lucro_%': round(lucro_pct, 2),
                'capital_atual': round(capital, 2)
            })
            em_posicao = False
            btc_em_maos = 0
            preco_compra = 0

# === RESULTADOS ===
historico_df = pd.DataFrame(historico)
historico_df.to_csv('../data/processed/backtest_resultado.csv', index=False)

lucro_total = ((capital - capital_inicial) / capital_inicial) * 100
print(f"\n📈 Backtest finalizado com spread de 1.2%")
print(f"💰 Lucro total: {lucro_total:.2f}%")
print(f"📊 Operações realizadas: {len(historico_df)//2} trades\n")

# === GRÁFICO ===
plt.figure(figsize=(14,6))
plt.plot(df['close'], label='Preço BTC/USDT', alpha=0.5)

compras = historico_df[historico_df['ação'] == 'compra']
vendas = historico_df[historico_df['ação'] == 'venda']

plt.scatter(compras['timestamp'], compras['preço'], marker='^', color='green', label='Compra', s=50)
plt.scatter(vendas['timestamp'], vendas['preço'], marker='v', color='red', label='Venda', s=50)

plt.title('Backtest RSI com Spread Realista - BTC/USDT (M5)')
plt.xlabel('Data')
plt.ylabel('Preço (USDT)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
