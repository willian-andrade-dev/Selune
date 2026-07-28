from Database.connection import conectar


def criar_progresso_crafting(player_id: int) -> None:
    """Cria o registro inicial de crafting do player (nível 1, 0 xp). Chamar na criação do player."""
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO player_crafting (player_id, nivel, xp)
        VALUES (%s, 1, 0)
        ON CONFLICT (player_id) DO NOTHING
    """, (player_id,))

    conexao.commit()
    cursor.close()
    conexao.close()

def carregar_crafting_skill(player_id: int) -> dict:
    """Retorna {"nivel": int, "xp": int}. Se o player ainda não tem registro, assume nível 1."""
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT nivel, xp FROM player_crafting WHERE player_id = %s
    """, (player_id,))
    linha = cursor.fetchone()

    cursor.close()
    conexao.close()

    if linha is None:
        return {"nivel": 1, "xp": 0}

    nivel, xp = linha
    return {"nivel": nivel, "xp": xp}

def atualizar_crafting_skill(player_id: int, nivel: int, xp: int) -> None:
    """Persiste nível e xp de crafting do player após um craft bem-sucedido."""
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE player_crafting SET nivel = %s, xp = %s WHERE player_id = %s
    """, (nivel, xp, player_id))

    conexao.commit()
    cursor.close()
    conexao.close()