import random
import string

def gerar_email_temporario():
    letras = string.ascii_lowercase + string.digits
    usuario = ''.join(random.choice(letras) for _ in range(10))
    return f"{usuario}@tmpmail.net"
