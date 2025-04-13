import subprocess
import time

ANDROID_IP = "192.168.183.253"  # ← o IP atual do seu hotspot

def trocar_ip_android(delay=30):
    print(f"[📶] Conectando ao Android ({ANDROID_IP})...")
    subprocess.run(["adb", "connect", f"{ANDROID_IP}:5555"])

    print("[🔌] Desligando dados móveis...")
    subprocess.run(["adb", "shell", "svc", "data", "disable"])

    print(f"[⏳] Aguardando {delay}s para liberar novo IP...")
    time.sleep(delay)

    print("[⚡] Ligando dados móveis novamente...")
    subprocess.run(["adb", "shell", "svc", "data", "enable"])

    print("[✅] Novo IP atribuído com sucesso!")

if __name__ == "__main__":
    trocar_ip_android()
