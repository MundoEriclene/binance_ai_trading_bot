import pandas as pd
import os
import matplotlib.pyplot as plt
import random

# === Funções ===
def is_martelo(candle):
    corpo = abs(candle["close"] - candle["open"])
    sombra_inf = min(candle["close"], candle["open"]) - candle["low"]
    sombra_sup = candle["high"] - max(candle["close"], candle["open"])
    return sombra_inf > 2 * corpo and sombra_sup < corpo * 0.5

def is_estrela_cadente(candle):
    corpo = abs(candle["close"] - candle["open"])
    sombra_sup = candle["high"] - max(candle["close"], candle["open"])
    sombra_inf = min(candle["close"], candle["open"]) - candle["low"]
    return sombra_sup > 2 * corpo and sombra_inf < corpo * 0.5 and candle["close"] < candle["open"]

def corpo_grande(candle, threshold=0.0007):
    return abs(candle["close"] - candle["open"]) >= threshold

def dentro_zona_ativa(preco, zonas):
    for faixa in zonas:
        if faixa.left < preco <= faixa.right:
            return True
    return False

# === Caminhos ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'eurusd_2024_2025.csv')
SAVE_PATH = os.path.join(BASE_DIR, 'data', 'resultados_fvg.csv')
GRAFICO_PATH = os.path.join(BASE_DIR, 'data', 'equity_curve_fvg.png')
RESUMO_PATH = os.path.join(BASE_DIR, 'data', 'resumo_fvg.txt')

# === Dados ===
df = pd.read_csv(DATA_PATH)
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.sort_values("timestamp").reset_index(drop=True)
df[["open", "high", "low", "close"]] = df[["open", "high", "low", "close"]].apply(pd.to_numeric, errors="coerce")

# === Market Profile ===
faixa_precos = pd.cut(df["close"], bins=100)
zona_frequente = faixa_precos.value_counts().sort_values(ascending=False).head(10)
zonas_ativas = zona_frequente.index.tolist()

# === Detectar FVG ===
fvg_zonas = []
for i in range(2, len(df)):
    candle = df.iloc[i - 2]
    high_2 = candle["high"]
    low_2 = candle["low"]
    low_0 = df.iloc[i]["low"]
    high_0 = df.iloc[i]["high"]
    time = df.iloc[i]["timestamp"]

    if not corpo_grande(candle):
        continue

    if low_0 > high_2 and dentro_zona_ativa(high_2, zonas_ativas):
        fvg_zonas.append({"tipo": "compra", "preco": high_2, "timestamp": time})
    elif high_0 < low_2 and dentro_zona_ativa(low_2, zonas_ativas):
        fvg_zonas.append({"tipo": "venda", "preco": low_2, "timestamp": time})

print(f"📌 Total de FVGs detectados: {len(fvg_zonas)}")

# === Estratégia ===
capital_inicial = 10000
capital = capital_inicial
trades = []
in_position = False

SL_PONTOS = 150
TP_MIN = 350
TP_MAX = 400
VALOR_PONTO = 1
VALOR_DO_PONTO_EM_PRECO = 0.0001

for i in range(3, len(df)):
    row = df.iloc[i]
    candle_anterior = df.iloc[i - 1]
    price = row["close"]
    time = row["timestamp"]

    for fvg in fvg_zonas:
        if fvg["timestamp"] >= time:
            continue

        if not in_position:
            if fvg["tipo"] == "compra" and price <= fvg["preco"] and is_martelo(candle_anterior):
                entry_price = price
                tipo = "compra"
                entry_time = time
                sl = entry_price - SL_PONTOS * VALOR_DO_PONTO_EM_PRECO
                tp_pontos = random.randint(TP_MIN, TP_MAX)
                tp = entry_price + tp_pontos * VALOR_DO_PONTO_EM_PRECO
                in_position = True
                break

            elif fvg["tipo"] == "venda" and price >= fvg["preco"] and is_estrela_cadente(candle_anterior):
                entry_price = price
                tipo = "venda"
                entry_time = time
                sl = entry_price + SL_PONTOS * VALOR_DO_PONTO_EM_PRECO
                tp_pontos = random.randint(TP_MIN, TP_MAX)
                tp = entry_price - tp_pontos * VALOR_DO_PONTO_EM_PRECO
                in_position = True
                break

        else:
            if tipo == "compra":
                if price <= sl:
                    pontos = round((price - entry_price) / VALOR_DO_PONTO_EM_PRECO, 1)
                    lucro = pontos * VALOR_PONTO
                    motivo = "Stop Loss"
                    in_position = False
                elif price >= tp:
                    pontos = round((price - entry_price) / VALOR_DO_PONTO_EM_PRECO, 1)
                    lucro = pontos * VALOR_PONTO
                    motivo = "Take Profit"
                    in_position = False
                else:
                    continue

            elif tipo == "venda":
                if price >= sl:
                    pontos = round((entry_price - price) / VALOR_DO_PONTO_EM_PRECO, 1)
                    lucro = pontos * VALOR_PONTO
                    motivo = "Stop Loss"
                    in_position = False
                elif price <= tp:
                    pontos = round((entry_price - price) / VALOR_DO_PONTO_EM_PRECO, 1)
                    lucro = pontos * VALOR_PONTO
                    motivo = "Take Profit"
                    in_position = False
                else:
                    continue

            capital += lucro
            trades.append({
                "tipo_trade": tipo,
                "entry_time": entry_time,
                "exit_time": time,
                "entry_price": round(entry_price, 5),
                "exit_price": round(price, 5),
                "pontos": pontos,
                "lucro_usd": round(lucro, 2),
                "capital": round(capital, 2),
                "motivo_saida": motivo,
                "fvg_origem": round(fvg["preco"], 5)
            })
            break

# === Resultado ===
if trades:
    result_df = pd.DataFrame(trades)
    result_df.to_csv(SAVE_PATH, index=False)

    total_trades = len(result_df)
    acertos = len(result_df[result_df["lucro_usd"] > 0])
    erros = total_trades - acertos
    taxa_acerto = (acertos / total_trades) * 100
    lucro_total = result_df["lucro_usd"].sum()
    retorno_pct = (capital - capital_inicial) / capital_inicial * 100
    drawdown = (result_df["capital"].cummax() - result_df["capital"]).max()
    result_df["data"] = pd.to_datetime(result_df["exit_time"]).dt.date
    diario = result_df.groupby("data")["lucro_usd"].sum()
    perda_max_diaria = diario.min()
    lucro_max_diario = diario.max()

    # Gráfico
    plt.figure(figsize=(10, 5))
    plt.plot(result_df["exit_time"], result_df["capital"], label="Equity Curve", color="blue")
    plt.title("Evolução do Capital - Estratégia FVG + Reversão + Zonas")
    plt.xlabel("Data")
    plt.ylabel("Saldo ($)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(GRAFICO_PATH)

    # Resumo
    resumo = f"""
📊 RELATÓRIO FINAL - FVG + Candle Reversão + Market Profile

Saldo Inicial:          $ {capital_inicial:,.2f}
Saldo Final:            $ {capital:,.2f}
Lucro Total:            $ {lucro_total:,.2f}
Retorno Total:          {retorno_pct:.2f}%
Lucro Máximo Diário:    $ {lucro_max_diario:,.2f}
Perda Máxima Diária:    $ {perda_max_diaria:,.2f}
Drawdown Máximo:        $ {drawdown:,.2f}
Taxa de Acerto:         {taxa_acerto:.2f}%
Total de Trades:        {total_trades}
Trades com Lucro:       {acertos}
Trades com Prejuízo:    {erros}

📄 CSV salvo em:         {SAVE_PATH}
🖼️ Gráfico salvo em:     {GRAFICO_PATH}
📝 Resumo salvo em:      {RESUMO_PATH}
"""
else:
    resumo = "⚠️ Nenhum trade executado. O robô não encontrou oportunidades com os critérios atuais."

# Mostrar e salvar
print(resumo)
with open(RESUMO_PATH, 'w', encoding='utf-8') as f:
    f.write(resumo.strip())

if trades:
    plt.show()
