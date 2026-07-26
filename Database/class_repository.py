from Database.connection import conectar
from Entities.classes import Classe
from Entities.habilidade import Habilidade

def carregar_classes() -> list:
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT id, nome, descricao, hp_base, mana_base, ataque_base, armadura_base,
               hp_regen_base, hp_regen_por_nivel, mana_regen_base, mana_regen_por_nivel
        FROM classes
    """)
    linhas = cursor.fetchall()
    cursor.close()
    conexao.close()

    classes = []
    for linha in linhas:
        (id, nome, descricao, hp_base, mana_base, ataque_base, armadura_base,
         hp_regen_base, hp_regen_por_nivel, mana_regen_base, mana_regen_por_nivel) = linha
        classes.append(Classe(
            id, nome, descricao, hp_base, mana_base, ataque_base, armadura_base,
            float(hp_regen_base), float(hp_regen_por_nivel),
            float(mana_regen_base), float(mana_regen_por_nivel)
        ))
    return classes

def carregar_habilidades() -> list:
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT id, classe_id, nome, descricao, nivel_requerido, custo_mana, tipo, valor, duracao_turnos, cooldown_turnos
        FROM habilidades
    """)
    linhas = cursor.fetchall()
    cursor.close()
    conexao.close()

    habilidades = []
    for linha in linhas:
        (id, classe_id, nome, descricao, nivel_requerido, custo_mana, tipo, valor, duracao_turnos, cooldown_turnos) = linha
        habilidades.append(Habilidade(id, classe_id, nome, descricao, nivel_requerido, custo_mana, tipo, valor, duracao_turnos, cooldown_turnos))
    return habilidades