import csv
import os
import time

def salvar_conta(pelotao_id, email, senha, nome, sobrenome, status, codigo, ip):
    # Caminho para o arquivo CSV onde vamos salvar os dados
    arquivo = f"contas_criadas_pelotao_{pelotao_id}.csv"
    
    # Verificar se o arquivo já existe para adicionar ou criar um novo
    file_exists = os.path.isfile(arquivo)
    
    # Abrir o arquivo no modo append (adicionar)
    with open(arquivo, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # Se o arquivo não existir, escrever o cabeçalho
        if not file_exists:
            writer.writerow(["Nome", "Sobrenome", "Email", "Senha", "Código", "Status", "IP", "Data"])
        
        # Adicionar os dados da nova conta
        writer.writerow([nome, sobrenome, email, senha, codigo, status, ip, time.strftime("%Y-%m-%d %H:%M:%S")])
        
    print(f"Conta {email} salva com sucesso!")
