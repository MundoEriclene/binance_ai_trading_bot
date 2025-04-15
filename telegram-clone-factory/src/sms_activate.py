import requests
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()
API_KEY = os.getenv("SMS_ACTIVATE_API_KEY")

class SMSActivate:
    def __init__(self):
        self.api_key = API_KEY
        self.base_url = "https://sms-activate.ru/stubs/handler_api.php"

    def get_phone_number(self, country="RU"):
        """Solicitar um número de telefone para validação"""
        url = f"{self.base_url}?api_key={self.api_key}&action=getNumber&country={country}&operator=any"
        response = requests.get(url)
        result = response.text
        if "ACCESS_NUMBER" in result:
            phone_number = result.split(":")[1]
            return phone_number
        else:
            raise Exception(f"Erro ao obter número: {result}")

    def get_code(self, phone_number):
        """Obter o código de verificação para o número"""
        url = f"{self.base_url}?api_key={self.api_key}&action=getStatus&phone={phone_number}"
        response = requests.get(url)
        result = response.text
        if "STATUS_OK" in result:
            code = result.split(":")[1]
            return code
        return None

    def get_balance(self):
        """Consulta o saldo da sua conta na SMS-Activate"""
        url = f"{self.base_url}?api_key={self.api_key}&action=getBalance"
        response = requests.get(url)
        result = response.text
        return result

    def get_prices(self):
        """Consulta os preços dos números de telefone disponíveis"""
        url = f"{self.base_url}?api_key={self.api_key}&action=getPrices"
        response = requests.get(url)
        result = response.text
        return result
