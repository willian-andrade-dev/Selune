from Database.connection import conectar

def carregar_eventos_localizacao(location_id: int) -> list[tuple[int, str, str, int]]:
    """Retorna [(event_id, nome, tipo, peso), ...] para a localização."""
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT e.id, e.nome, e.tipo, le.peso
        FROM location_events le
        JOIN events e ON e.id = le.event_id
        WHERE le.location_id = %s
    """, (location_id,))
    linhas = cursor.fetchall()
    cursor.close()
    conexao.close()
    return linhas

def sortear_material(raridade: str, familia: str | None = None) -> tuple[int, str] | None:
    """Sorteia um item Loot/Material da raridade informada. Retorna (id, nome) ou None."""
    conexao = conectar()
    cursor = conexao.cursor()
    if familia is not None:
        cursor.execute("""
            SELECT id, nome FROM items
            WHERE tipo = 'Loot' AND subtipo = 'Material' AND raridade = %s AND familia_material = %s
            ORDER BY RANDOM() LIMIT 1
        """, (raridade, familia))
    else:
        cursor.execute("""
            SELECT id, nome FROM items
            WHERE tipo = 'Loot' AND subtipo = 'Material' AND raridade = %s
            ORDER BY RANDOM() LIMIT 1
        """, (raridade,))
    linha = cursor.fetchone()
    cursor.close()
    conexao.close()
    return linha