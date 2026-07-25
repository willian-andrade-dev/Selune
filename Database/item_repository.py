from Database.connection import conectar
from Entities.item import Weapon, Armadura, Consumivel, Loot, Acessorio


def criar_item(nome: str, tipo: str, valor: int, nivel_requerido: int, descricao: str,
               funcao: str = None, dano: int = None, armadura: int = None,
               raridade: str = "Comum", subtipo: str = None) -> int:
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
        INSERT INTO items (nome, tipo, valor, nivel_requerido, descricao, funcao, dano, armadura, raridade, subtipo)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (nome) DO NOTHING
        RETURNING id
    """, (nome, tipo, valor, nivel_requerido, descricao, funcao, dano, armadura, raridade, subtipo))

    item_id = cursor.fetchone()[0]

    conexao.commit()
    cursor.close()
    conexao.close()

    return item_id


def adicionar_efeito_item(item_id: int, nome_atributo: str, valor: float, percentual: bool = False) -> None:
    """Vincula um bônus (item_effects) a um item já existente, pelo nome do atributo."""
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT id FROM attributes WHERE nome = %s", (nome_atributo,))
    atributo = cursor.fetchone()
    if atributo is None:
        print(f"Atributo '{nome_atributo}' não existe em attributes, pulando.")
        cursor.close()
        conexao.close()
        return

    cursor.execute("""
        INSERT INTO item_effects (item_id, attribute_id, valor, percentual)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (item_id, attribute_id) DO NOTHING
    """, (item_id, atributo[0], valor, percentual))

    conexao.commit()
    cursor.close()
    conexao.close()


def carregar_itens() -> dict:
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome, tipo, valor, nivel_requerido, descricao, funcao, dano, armadura, raridade, subtipo
        FROM items
    """)
    linhas_itens = cursor.fetchall()

    # carrega todos os efeitos de uma vez (evita N+1 queries) e agrupa por item_id
    cursor.execute("""
        SELECT ie.item_id, a.nome, ie.valor, ie.percentual
        FROM item_effects ie
        JOIN attributes a ON a.id = ie.attribute_id
    """)
    linhas_efeitos = cursor.fetchall()

    cursor.close()
    conexao.close()

    efeitos_por_item = {}
    for item_id, nome_atributo, valor, percentual in linhas_efeitos:
        efeitos_por_item.setdefault(item_id, []).append({
            "atributo": nome_atributo,
            "valor": float(valor),
            "percentual": percentual
        })

    itens = {}
    for linha in linhas_itens:
        id, nome, tipo, valor, nivel_requerido, descricao, funcao, dano, armadura, raridade, subtipo = linha
        efeitos = efeitos_por_item.get(id, [])

        if tipo == "Arma":
            item = Weapon(nome, valor, descricao, nivel_requerido, raridade, dano, efeitos)
        elif tipo == "Armadura":
            item = Armadura(nome, valor, descricao, nivel_requerido, raridade, armadura, efeitos)
        elif tipo == "Consumivel":
            item = Consumivel(nome, valor, descricao, nivel_requerido, raridade, funcao)
        elif tipo == "Acessorio":
            item = Acessorio(nome, valor, descricao, nivel_requerido, raridade, subtipo, efeitos)
        else:  # Loot
            item = Loot(nome, valor, descricao, nivel_requerido, raridade)

        item.id = id
        itens[id] = item

    return itens