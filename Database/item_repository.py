from Database.connection import conectar
from Entities.item import Weapon, Armadura, Consumivel, Loot

def criar_item(nome: str, tipo: str, valor: int, descricao: str, armadura: int=None, dano: int=None, funcao: str=None, propriedade: str=None) -> int:
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT id FROM items WHERE nome = %s", (nome,))
    existe = cursor.fetchone()

    if existe:
        print(f"{nome} já existe no banco, pulando.")
        cursor.close()
        conexao.close()
        return existe[0]

    cursor.execute("""
        INSERT INTO items (nome, tipo, valor, descricao, armadura, dano, funcao, propriedade)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (nome) DO NOTHING
        RETURNING id
    """, (nome, tipo, valor, descricao, armadura, dano, funcao, propriedade))

    item_id = cursor.fetchone()[0]

    conexao.commit()
    cursor.close()
    conexao.close()

    return item_id

def carregar_itens() -> dict:
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome, tipo, valor, descricao, armadura, dano, funcao, propriedade FROM items")
    linhas = cursor.fetchall()
    cursor.close()
    conexao.close()

    itens = {}
    for linha in linhas:
        id, nome, tipo, valor, descricao, armadura, dano, funcao, propriedade = linha
        if tipo == "Arma":
            item = Weapon(nome, valor, descricao, dano)
        elif tipo == "Armadura":
            item = Armadura(nome, valor, descricao, armadura)
        elif tipo == "Consumivel":
            item = Consumivel(nome, valor, descricao, funcao)
        else:  # Loot
            item = Loot(nome, valor, descricao)
        item.id = id  # guarda o id do banco no próprio objeto
        itens[id] = item

    return itens
