import os
from dotenv import load_dotenv

def carregar_configuracoes(env_path):
    load_dotenv(env_path)
    return {
        "email": os.getenv("GMAIL_USER1"),
        "senha": os.getenv("GMAIL_PASSWORD1"),
        "nome": os.getenv("GMAIL_NAME"),
        "curriculo": os.getenv("CURRICULO_PATH"),
        "mensagem_html": os.getenv("MENSAGEM_HTML_PATH")
    }
