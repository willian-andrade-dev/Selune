from Database.connection import conectar
from Entities.monster import Monstro

def criar_monstro(nome, hp, loot_item_id, ataque, xp, ouro, location_ids):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT id FROM monsters WHERE nome = %s", (nome,))
    existe = cursor.fetchone()

    if existe:
        print(f"{nome} já existe no banco, pulando.")
        cursor.close()
        conexao.close()
        return existe[0]

    cursor.execute("""
        INSERT INTO monsters (nome, hp, loot_item_id, ataque, xp, ouro)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (nome, hp, loot_item_id, ataque, xp, ouro))

    monster_id = cursor.fetchone()[0]

    for location_id in location_ids:
        cursor.execute("""
            INSERT INTO monster_locations (monster_id, location_id)
            VALUES (%s, %s)
        """, (monster_id, location_id))

    conexao.commit()
    cursor.close()
    conexao.close()

    return monster_id

def carregar_monstros(itens):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome, hp, loot_item_id, ataque, xp, ouro FROM monsters")
    linhas = cursor.fetchall()
    cursor.close()
    conexao.close()

    monstros = []
    for linha in linhas:
        id, nome, hp, loot_item_id, ataque, xp, ouro = linha
        loot = itens.get(loot_item_id)  # pega o objeto Item já carregado, ou None
        monstro = Monstro(nome, hp, loot, ataque, xp, ouro)
        monstros.append(monstro)

    return monstros