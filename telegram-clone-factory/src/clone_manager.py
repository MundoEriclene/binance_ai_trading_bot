from telethon import TelegramClient
from sms_activate import SMSActivate
from proxy_manager import ProxyManager
from trocar_ip import trocar_ip_android
import random
import time
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

class CloneManager:
    def __init__(self, sms_api_key, config_file="config.json"):
        self.sms_activate = SMSActivate()
        self.proxy_manager = ProxyManager(config_file)
        self.client = None

    def create_telegram_account(self):
        """Criar uma nova conta no Telegram usando número virtual"""
        print("Obtendo número de telefone...")
        phone_number = self.sms_activate.get_phone_number()

        print(f"Número recebido: {phone_number}")
        print("Obtendo código de verificação...")
        code = self.sms_activate.get_code(phone_number)

        if not code:
            print("Não foi possível obter o código de verificação.")
            return None

        print(f"Código recebido: {code}")
        trocar_ip_android()  # Trocar IP antes de criar a conta
        proxy = self.proxy_manager.get_random_proxy()
        print(f"Usando proxy: {proxy}")

        self.client = TelegramClient('anon', 12345, 67890, proxy=proxy)
        self.client.start(phone_number, code)

        return self.client
