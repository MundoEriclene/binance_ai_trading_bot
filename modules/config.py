import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do .env
env_path = os.path.join(os.path.dirname(__file__), '../config/.env')
load_dotenv(env_path)

# Configuração da API da OKX
OKX_API_KEY = os.getenv("OKX_API_KEY")
OKX_API_SECRET = os.getenv("OKX_API_SECRET")
OKX_API_PASSPHRASE = os.getenv("OKX_API_PASSPHRASE")

# Configuração da API da Yobit
YOBIT_API_KEY = os.getenv("YOBIT_API_KEY")
YOBIT_API_SECRET = os.getenv("YOBIT_API_SECRET")

# Endereços para Transferência
OKX_WALLET_BNB = os.getenv("OKX_WALLET_BNB")
YOBIT_WALLET_USDT = os.getenv("YOBIT_WALLET_USDT")

# Configuração de Operações
TRADE_AMOUNT_BNB = float(os.getenv("TRADE_AMOUNT_BNB", "1"))
NETWORK = os.getenv("NETWORK", "ERC20")

# Verificação básica das credenciais
if not OKX_API_KEY or not OKX_API_SECRET or not YOBIT_API_KEY:
    raise ValueError("❌ ERRO: Certifique-se de configurar corretamente suas credenciais no arquivo .env!")

print("✅ Configuração carregada com sucesso!")
