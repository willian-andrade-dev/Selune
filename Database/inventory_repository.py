from Database.connection import conectar

def adicionar_item_inventario(player_id: int, item_id: int, quantidade: int=1) -> None:
    conexao = conectar()
    cursor = conexao.cursor()

    # verifica se o player já tem esse item
    cursor.execute("""
        SELECT id, quantidade FROM inventory 
        WHERE player_id = %s AND item_id = %s
    """, (player_id, item_id))
    existe = cursor.fetchone()

    if existe:
        inventory_id, quantidade_atual = existe
        nova_quantidade = quantidade_atual + quantidade
        cursor.execute("""
            UPDATE inventory SET quantidade = %s WHERE id = %s
        """, (nova_quantidade, inventory_id))
    else:
        cursor.execute("""
            INSERT INTO inventory (player_id, item_id, quantidade)
            VALUES (%s, %s, %s)
        """, (player_id, item_id, quantidade))

    conexao.commit()
    cursor.close()
    conexao.close()

def carregar_inventario_jogador(player_id: int, itens: dict) -> list:
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT item_id, quantidade FROM inventory WHERE player_id = %s
    """, (player_id,))
    linhas = cursor.fetchall()
    cursor.close()
    conexao.close()

    itens_carregados = []
    for item_id, quantidade in linhas:
        item = itens.get(item_id)
        if item is not None:
            for _ in range(quantidade):
                itens_carregados.append(item)
    return itens_carregados

def remover_item_inventario(player_id: int, item_id: int, quantidade: int = 1) -> None:
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, quantidade FROM inventory
        WHERE player_id = %s AND item_id = %s
    """, (player_id, item_id))
    existe = cursor.fetchone()

    if existe:
        inventory_id, quantidade_atual = existe
        nova_quantidade = quantidade_atual - quantidade
        if nova_quantidade <= 0:
            cursor.execute("DELETE FROM inventory WHERE id = %s", (inventory_id,))
        else:
            cursor.execute("UPDATE inventory SET quantidade = %s WHERE id = %s", (nova_quantidade, inventory_id))

    conexao.commit()
    cursor.close()
    conexao.close()