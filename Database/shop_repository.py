from Database.connection import conectar
from Database.inventory_repository import adicionar_item_inventario, remover_item_inventario


def listar_itens_loja(tipo: str = None) -> list:
    """Retorna itens disponíveis na loja, opcionalmente filtrados por tipo (Arma, Armadura, Consumivel, Acessorio)."""
    conexao = conectar()
    cursor = conexao.cursor()

    if tipo:
        cursor.execute("""
            SELECT i.id, i.nome, i.tipo, i.raridade, i.nivel_requerido, si.preco_compra, si.preco_venda, si.compravel
            FROM shop_items si
            JOIN items i ON i.id = si.item_id
            WHERE si.disponivel = TRUE AND i.tipo = %s
            ORDER BY i.nivel_requerido
        """, (tipo,))
    else:
        cursor.execute("""
            SELECT i.id, i.nome, i.tipo, i.raridade, i.nivel_requerido, si.preco_compra, si.preco_venda, si.compravel
            FROM shop_items si
            JOIN items i ON i.id = si.item_id
            WHERE si.disponivel = TRUE
            ORDER BY i.tipo, i.nivel_requerido
        """)

    linhas = cursor.fetchall()
    cursor.close()
    conexao.close()

    itens = []
    for item_id, nome, tipo_item, raridade, nivel_requerido, preco_compra, preco_venda, compravel in linhas:
        itens.append({
            "item_id": item_id,
            "nome": nome,
            "tipo": tipo_item,
            "raridade": raridade,
            "nivel_requerido": nivel_requerido,
            "preco_compra": preco_compra,
            "preco_venda": preco_venda,
            "compravel": compravel,
        })
    return itens


def listar_inventario_vendavel(player_id: int) -> list:
    """Retorna os itens do inventário do player que podem ser vendidos na loja."""
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT i.id, i.nome, i.tipo, i.raridade, inv.quantidade, si.preco_venda
        FROM inventory inv
        JOIN items i ON i.id = inv.item_id
        JOIN shop_items si ON si.item_id = i.id
        WHERE inv.player_id = %s AND si.disponivel = TRUE
        ORDER BY i.tipo, i.nome
    """, (player_id,))

    linhas = cursor.fetchall()
    cursor.close()
    conexao.close()

    itens = []
    for item_id, nome, tipo, raridade, quantidade, preco_venda in linhas:
        itens.append({
            "item_id": item_id,
            "nome": nome,
            "tipo": tipo,
            "raridade": raridade,
            "quantidade": quantidade,
            "preco_venda": preco_venda,
        })
    return itens


def comprar_item(player_id: int, item_id: int, quantidade: int = 1) -> tuple:
    """Tenta comprar `quantidade` unidades do item pelo id.
    Retorna (sucesso: bool, mensagem: str, gold_gasto: int)."""
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT i.nome, si.preco_compra, si.compravel, si.disponivel
        FROM shop_items si
        JOIN items i ON i.id = si.item_id
        WHERE si.item_id = %s
    """, (item_id,))
    resultado = cursor.fetchone()

    if resultado is None:
        cursor.close()
        conexao.close()
        return False, "Item não encontrado na loja.", 0

    nome, preco_compra, compravel, disponivel = resultado

    if not disponivel or not compravel:
        cursor.close()
        conexao.close()
        return False, f"'{nome}' não está disponível para compra.", 0

    total = preco_compra * quantidade

    cursor.execute("SELECT gold FROM players WHERE id = %s", (player_id,))
    resultado_gold = cursor.fetchone()
    if resultado_gold is None:
        cursor.close()
        conexao.close()
        return False, "Player não encontrado.", 0

    gold_atual = resultado_gold[0]
    if gold_atual < total:
        cursor.close()
        conexao.close()
        return False, f"Gold insuficiente. Necessário: {total}, disponível: {gold_atual}.", 0

    cursor.execute("UPDATE players SET gold = gold - %s WHERE id = %s", (total, player_id))
    conexao.commit()
    cursor.close()
    conexao.close()

    adicionar_item_inventario(player_id, item_id, quantidade)

    return True, f"Você comprou {quantidade}x {nome} por {total} gold.", total


def vender_item(player_id: int, item_id: int, quantidade: int = 1) -> tuple:
    """Tenta vender `quantidade` unidades do item pelo id.
    Retorna (sucesso: bool, mensagem: str, gold_ganho: int)."""
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT i.nome, si.preco_venda, si.disponivel
        FROM shop_items si
        JOIN items i ON i.id = si.item_id
        WHERE si.item_id = %s
    """, (item_id,))
    resultado = cursor.fetchone()

    if resultado is None:
        cursor.close()
        conexao.close()
        return False, "Item não é reconhecido pela loja.", 0

    nome, preco_venda, disponivel = resultado

    if not disponivel:
        cursor.close()
        conexao.close()
        return False, f"'{nome}' não está disponível na loja no momento.", 0

    cursor.execute("""
        SELECT quantidade FROM inventory WHERE player_id = %s AND item_id = %s
    """, (player_id, item_id))
    resultado_inventario = cursor.fetchone()
    quantidade_possuida = resultado_inventario[0] if resultado_inventario else 0

    if quantidade_possuida < quantidade:
        cursor.close()
        conexao.close()
        return False, f"Você só possui {quantidade_possuida}x {nome}.", 0

    total = preco_venda * quantidade

    cursor.execute("UPDATE players SET gold = gold + %s WHERE id = %s", (total, player_id))
    conexao.commit()
    cursor.close()
    conexao.close()

    remover_item_inventario(player_id, item_id, quantidade)

    return True, f"Você vendeu {quantidade}x {nome} por {total} gold.", total