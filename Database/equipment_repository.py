from Database.connection import conectar

def equipar_item(player_id: int, slot: str, item_id: int) -> None:
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO player_equipment (player_id, slot, item_id)
        VALUES (%s, %s, %s)
        ON CONFLICT (player_id, slot) DO UPDATE SET item_id = EXCLUDED.item_id
    """, (player_id, slot, item_id))
    conexao.commit()
    cursor.close()
    conexao.close()

def desequipar_item(player_id: int, slot: str) -> None:
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM player_equipment WHERE player_id = %s AND slot = %s", (player_id, slot))
    conexao.commit()
    cursor.close()
    conexao.close()

def buscar_equipamento(player_id: int) -> dict[str, int]:
    """Retorna {slot: item_id} de tudo que o player tem equipado."""
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT slot, item_id FROM player_equipment WHERE player_id = %s", (player_id,))
    linhas = cursor.fetchall()
    cursor.close()
    conexao.close()
    return dict(linhas)