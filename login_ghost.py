from telethon.sync import TelegramClient
from dotenv import load_dotenv
import os

# Carrega variáveis do .env
load_dotenv()
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

# Nome da sessão (será salvo como ghost_real.session)
client = TelegramClient("ghost_real", api_id, api_hash)

async def main():
    me = await client.get_me()
    print(f"✅ Logado como: {me.first_name} | ID: {me.id} | Username: @{me.username}")

# Executa o login
with client:
    client.loop.run_until_complete(main())
