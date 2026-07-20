from Database.connection import conectar

def registrar_combate(player_id: int, monster_id: int, xp_ganho: int, gold_ganho: int, vitoria: bool, duracao_ms: int) -> None:
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO combat_logs (player_id, monster_id, xp_ganho, gold_ganho, vitoria, duracao_ms)
        VALUES(%s, %s, %s, %s, %s, %s)
    """, (player_id, monster_id, xp_ganho, gold_ganho, vitoria, duracao_ms))

    conexao.commit()
    cursor.close()
    conexao.close()
    