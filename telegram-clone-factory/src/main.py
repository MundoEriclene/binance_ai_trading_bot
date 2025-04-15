from clone_manager import CloneManager
import time

def main():
    sms_api_key = "SUA_CHAVE_API_SMS_ACTIVATE"  # Substitua por uma variável de ambiente, se preferir
    clone_manager = CloneManager(sms_api_key)

    contas_criadas = 0
    total_contas = 10000

    while contas_criadas < total_contas:
        print(f"Criando conta {contas_criadas + 1}/{total_contas}")
        client = clone_manager.create_telegram_account()

        if client:
            print(f"Conta criada com sucesso!")
            contas_criadas += 1
        else:
            print("Falha ao criar conta.")
        
        time.sleep(5)  # Espera de 5 segundos entre as tentativas

if __name__ == "__main__":
    main()
