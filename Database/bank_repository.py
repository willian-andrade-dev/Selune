from Database.connection import conectar


def buscar_saldo_banco(player_id: int) -> int:
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT gold_banco FROM players WHERE id = %s", (player_id,))
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    return resultado[0] if resultado else 0


def depositar(player_id: int, valor: int) -> None:
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        UPDATE players SET gold = gold - %s, gold_banco = gold_banco + %s WHERE id = %s
    """, (valor, valor, player_id))
    conexao.commit()
    cursor.close()
    conexao.close()


def sacar(player_id: int, valor: int) -> None:
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        UPDATE players SET gold = gold + %s, gold_banco = gold_banco - %s WHERE id = %s
    """, (valor, valor, player_id))
    conexao.commit()
    cursor.close()
    conexao.close()