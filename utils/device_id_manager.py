import random
import string

def gerar_device_id():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(16))

def gerar_device_fingerprint():
    modelos = ['iPhone X', 'Samsung S21', 'Pixel 6', 'Xiaomi Redmi 10', 'Moto G30']
    sistemas = ['iOS 16.1', 'Android 11', 'Android 12', 'Android 13']
    versoes_app = ['9.2.1', '9.3.2', '9.4.1', '9.4.3']
    idiomas = ['pt', 'en', 'es', 'fr', 'it']

    fingerprint = {
        'device_model': random.choice(modelos),
        'system_version': random.choice(sistemas),
        'app_version': random.choice(versoes_app),
        'lang_code': random.choice(idiomas),
        'device_id': gerar_device_id()
    }
    return fingerprint

# Exemplo de uso
if __name__ == "__main__":
    fingerprint = gerar_device_fingerprint()
    print("📱 Fingerprint gerado:")
    for chave, valor in fingerprint.items():
        print(f"   {chave}: {valor}")
