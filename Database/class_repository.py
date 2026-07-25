from Database.connection import conectar
from Entities.classes import Classe, Habilidade

def carregar_classes() -> list:
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome, descricao, hp_base, mana_base, ataque_base, armadura_base FROM classes")
    linhas = cursor.fetchall()
    cursor.close()
    conexao.close()

    classes = []
    for linha in linhas:
        id, nome, descricao, hp_base, mana_base, ataque_base, armadura_base = linha
        classes.append(Classe(id, nome, descricao, hp_base, mana_base, ataque_base, armadura_base))
    return classes

def carregar_habilidades() -> list:
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT id, classe_id, nome, descricao, nivel_requerido, custo_mana, tipo, valor, duracao_turnos
        FROM habilidades
    """)
    linhas = cursor.fetchall()
    cursor.close()
    conexao.close()

    habilidades = []
    for linha in linhas:
        id, classe_id, nome, descricao, nivel_requerido, custo_mana, tipo, valor, duracao_turnos = linha
        habilidades.append(Habilidade(id, classe_id, nome, descricao, nivel_requerido, custo_mana, tipo, valor, duracao_turnos))
    return habilidades