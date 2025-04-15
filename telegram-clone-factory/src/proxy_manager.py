import random
import json
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

class ProxyManager:
    def __init__(self, config_file="config.json"):
        with open(config_file, "r") as f:
            self.config = json.load(f)
        self.proxies = self.config.get("proxy_list", [])

    def get_random_proxy(self):
        """Retorna um proxy aleatório da lista"""
        return random.choice(self.proxies) if self.proxies else None
