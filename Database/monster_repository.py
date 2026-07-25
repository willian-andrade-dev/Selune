from Database.connection import conectar
from Entities.monster import Monstro


def criar_monstro(nome: str, hp: int, ataque: int, xp: int, ouro: int, location_ids: list) -> int:
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
        INSERT INTO monsters (nome, hp, ataque, xp, ouro)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
    """, (nome, hp, ataque, xp, ouro))

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


def criar_drop_monstro(monster_id: int, item_id: int, chance_drop: float) -> None:
    """Vincula um possível drop (monster_drops) a um monstro já existente."""
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO monster_drops (monster_id, item_id, chance_drop)
        VALUES (%s, %s, %s)
        ON CONFLICT (monster_id, item_id) DO NOTHING
    """, (monster_id, item_id, chance_drop))

    conexao.commit()
    cursor.close()
    conexao.close()


def carregar_monstros(itens: dict) -> list:
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT id, nome, hp, ataque, xp, ouro FROM monsters")
    linhas_monstros = cursor.fetchall()

    cursor.execute("SELECT monster_id, item_id, chance_drop FROM monster_drops")
    linhas_drops = cursor.fetchall()

    cursor.close()
    conexao.close()

    drops_por_monstro = {}
    for monster_id, item_id, chance in linhas_drops:
        item = itens.get(item_id)
        if item is not None:
            drops_por_monstro.setdefault(monster_id, []).append((item, float(chance)))

    monstros = []
    for linha in linhas_monstros:
        id, nome, hp, ataque, xp, ouro = linha
        monstro = Monstro(nome, hp, ataque, xp, ouro)
        monstro.id = id
        monstro.drops = drops_por_monstro.get(id, [])
        monstros.append(monstro)

    return monstros