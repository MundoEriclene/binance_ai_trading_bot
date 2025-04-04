import os
import json
import time
import random
import asyncio
import requests
from dotenv import load_dotenv
from telethon import TelegramClient, events

# Carregar variáveis de ambiente
load_dotenv()
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
openai_key = os.getenv("OPENAI_API_KEY")

# Inicializar cliente
client = TelegramClient("ericlene_principal", api_id, api_hash)

# Caminho do arquivo de memória
MEMORIA_PATH = "usuarios.json"

# Carregar memória de usuários
def carregar_memoria():
    if os.path.exists(MEMORIA_PATH):
        with open(MEMORIA_PATH, "r") as f:
            return json.load(f)
    return {}

# Salvar memória
def salvar_memoria(memoria):
    with open(MEMORIA_PATH, "w") as f:
        json.dump(memoria, f, indent=4)

# Gerar código novo
def gerar_novo_codigo(memoria):
    codigos = [int(info["codigo"]) for info in memoria.values() if info.get("codigo", "").isdigit()]
    novo_codigo = max(codigos, default=0) + 1
    return str(novo_codigo).zfill(2)

# Obter ou criar dados do usuário
def obter_usuario(user_id, username, memoria):
    if str(user_id) not in memoria:
        memoria[str(user_id)] = {
            "username": username,
            "codigo": gerar_novo_codigo(memoria),
            "ultima_msg": ""
        }
        salvar_memoria(memoria)
    return memoria[str(user_id)]

# Gerar resposta com OpenAI
def gerar_resposta_ericlene(pergunta, contexto=""):
    try:
        resposta = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {openai_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-3.5-turbo",
                "temperature": 0.85,
                "max_tokens": 150,
                "messages": [
                    {"role": "system", "content": (
                        "Você é Ericlene De Sousa, um humano carismático, observador, direto, misterioso. "
                        "Nunca diga que é uma IA. Sempre responda como se fosse o próprio Ericlene. "
                        "Se perguntarem 'qual é nosso código', responda com o código correto salvo. "
                        "Se perguntarem 'qual foi minha última mensagem', diga a última registrada." )},
                    {"role": "user", "content": f"{contexto}\n\n{pergunta}".strip()}
                ]
            }
        )
        if resposta.status_code == 200:
            return resposta.json()["choices"][0]["message"]["content"].strip()
        else:
            return "Tá difícil agora, tenta de novo depois."
    except:
        return "Deu um bug aqui... manda de novo pra ver se vai."

# Evento principal
@client.on(events.NewMessage(incoming=True))
async def responder(event):
    if event.is_private and not event.out:
        user = await event.get_sender()
        user_id = user.id
        username = user.username or f"id_{user_id}"
        texto = event.text.strip()

        print(f"📩 [{username}] {texto}")

        memoria = carregar_memoria()
        dados = obter_usuario(user_id, username, memoria)
        contexto = dados.get("ultima_msg", "")

        # Respostas fixas para perguntas diretas
        if "código" in texto.lower():
            resposta = f"Nosso código de conversa é {dados['codigo']}. Se eu não disser isso, não sou o verdadeiro."
        elif "última mensagem" in texto.lower():
            resposta = f"Sua última mensagem registrada foi: '{contexto}'"
        else:
            tempo = random.uniform(4, 9)
            print(f"⌛ Esperando {tempo:.1f}s para simular digitação...")
            await asyncio.sleep(tempo)

            resposta = gerar_resposta_ericlene(texto, contexto=contexto)

        memoria[str(user_id)]["ultima_msg"] = texto
        salvar_memoria(memoria)

        await asyncio.sleep(random.uniform(1, 3))
        await event.reply(resposta)
        print("✅ Respondido com sucesso!")

client.start()
print("🤖 IA do Ericlene ativada com memória e códigos únicos...")
client.run_until_disconnected()