import os
import json
import datetime
from core.notificacoes import enviar_email

CAMINHO_LOG = "core/logs/log_diario.json"

def carregar_log():
    if not os.path.exists(CAMINHO_LOG):
        return []
    with open(CAMINHO_LOG, "r") as f:
        return json.load(f)

def gerar_relatorio(tipo="Diário"):
    log = carregar_log()
    if not log:
        return "Nenhuma atividade registrada no período."

    # Ordenar log por timestamp
    log.sort(key=lambda x: x.get("timestamp", ""))

    hoje = datetime.datetime.utcnow().date()
    resumo = f"🤖 *RoboTrader V1.8 – Relatório {tipo.upper()}*\n📅 {hoje.strftime('%d/%m/%Y')}\n\n"

    total_compras = 0
    total_vendas = 0
    total_erros = 0
    lucro_total = 0.0

    for item in log:
        raw_data = item.get("timestamp", "desconhecido")
        try:
            data = datetime.datetime.fromisoformat(raw_data).strftime("%d/%m/%Y %H:%M")
        except:
            data = raw_data

        if item["tipo"] == "compra":
            resumo += f"🟢 *Compra* — {data} a `{item['preco']:.2f}` USDT\n"
            total_compras += 1

        elif item["tipo"] == "venda":
            resumo += f"🔴 *Venda* — {data} a `{item['preco']:.2f}` USDT | Lucro: `{item['lucro']:.2f}` USDT\n"
            lucro_total += item['lucro']
            total_vendas += 1

        elif item["tipo"] == "erro":
            resumo += f"⚠️ *Erro* — {data}:\n> {item['mensagem']}\n"
            total_erros += 1

    resumo += "\n📌 *Resumo Final*\n"
    resumo += f"- Compras realizadas: `{total_compras}`\n"
    resumo += f"- Vendas executadas: `{total_vendas}`\n"
    resumo += f"- Erros detectados: `{total_erros}`\n"
    resumo += f"- Lucro total estimado: `{lucro_total:.2f}` USDT\n"

    resumo += "\n✅ Robô ativo e rodando normalmente.\n🚀 Continue acompanhando no Telegram para alertas em tempo real."

    return resumo

def enviar_relatorio(tipo="Diário"):
    resumo = gerar_relatorio(tipo)
    assunto = f"📬 Relatório {tipo} do RoboTrader"
    enviar_email(assunto, resumo)
