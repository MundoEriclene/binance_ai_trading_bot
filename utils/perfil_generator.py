import os
import random

NOMES_ARQUIVO = 'config/nomes.txt'
USADOS_NOMES = 'logs/nomes_usados.txt'
USADOS_BIOS = 'logs/bios_usadas.txt'

BIOS = [
    "Apaixonado por tecnologia 📱",
    "Vivendo um dia de cada vez 🌍",
    "Aprendendo sempre 🧠",
    "Guerreiro digital 🕶️",
    "Conectado com o mundo 🤖",
    "Explorador silencioso 👣",
    "Em busca de algo maior 💡"
]

EMOJIS = ['🧠', '😎', '🔥', '💻', '🌌', '👁️', '⚡', '👨‍💻', '🧬']

def carregar_linhas(caminho):
    if not os.path.exists(caminho):
        return set()
    with open(caminho, 'r', encoding='utf-8') as f:
        return {linha.strip() for linha in f if linha.strip()}

def salvar_linha(caminho, texto):
    with open(caminho, 'a', encoding='utf-8') as f:
        f.write(texto + '\n')

def gerar_perfil():
    nomes = carregar_linhas(NOMES_ARQUIVO)
    nomes_usados = carregar_linhas(USADOS_NOMES)
    bios_usadas = carregar_linhas(USADOS_BIOS)

    nomes_disponiveis = list(nomes - nomes_usados)
    bios_disponiveis = list(set(BIOS) - bios_usadas)

    if not nomes_disponiveis:
        raise Exception("❌ Todos os nomes foram usados.")
    if not bios_disponiveis:
        raise Exception("❌ Todas as bios foram usadas.")

    nome_completo = random.choice(nomes_disponiveis)
    bio = random.choice(bios_disponiveis)
    emoji = random.choice(EMOJIS)

    salvar_linha(USADOS_NOMES, nome_completo)
    salvar_linha(USADOS_BIOS, bio)

    return {
        'nome_completo': nome_completo,
        'primeiro_nome': nome_completo.split()[0],
        'sobrenome': ' '.join(nome_completo.split()[1:]),
        'bio': bio,
        'emoji': emoji
    }

# Exemplo de uso
if __name__ == "__main__":
    perfil = gerar_perfil()
    print(f"🧑 Nome: {perfil['nome_completo']}")
    print(f"📝 Bio: {perfil['bio']} {perfil['emoji']}")
