# scripts/salvar_conta.py

import os
from datetime import datetime

def salvar_conta(pelotao_id, email, senha, nome, sobrenome, status, codigo):
    pasta = f"../pelotoes/pelotao_{str(pelotao_id).zfill(2)}"
    os.makedirs(pasta, exist_ok=True)

    arquivo_contas = os.path.join(pasta, "contas.txt")
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(arquivo_contas, "a") as f:
        f.write(
            f"[{agora}] | {email} | {senha} | {nome} {sobrenome} | {status} | Código: {codigo or 'N/A'}\n"
        )

    print(f"[💾] Conta salva no pelotão {pelotao_id}: {email}")
