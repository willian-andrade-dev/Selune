from Database.connection import conectar

def adicionar_item_inventario(player_id, item_id, quantidade=1):
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

