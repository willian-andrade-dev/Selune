from Database.connection import conectar
from Entities.player import Player

def criar_player(nome, hp, hp_maximo, mana, gold, xp, xp_para_upar, level, ataque_base, ataque, armadura, armadura_base):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO players (nome, hp, hp_maximo, mana, gold, xp, xp_para_upar, level, ataque_base, ataque, armadura, armadura_base)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (nome, hp, hp_maximo, mana, gold, xp, xp_para_upar, level, ataque_base, ataque, armadura, armadura_base))

    player_id = cursor.fetchone()[0]

    conexao.commit()
    cursor.close()
    conexao.close()

    return player_id

def buscar_player(id_player):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM players WHERE id = %s", (id_player,))
    linha = cursor.fetchone()

    cursor.close()
    conexao.close()

    if linha is None:
        return None
    
    id, nome, hp, hp_maximo, mana, gold, xp, xp_para_upar, level, ataque_base, ataque, armadura, armadura_base = linha
    player = Player(nome, hp, mana, gold, xp, level, ataque_base, armadura_base)
    player.id = id
    player.hp_maximo = hp_maximo
    player.xp_para_upar = xp_para_upar
    player.ataque = ataque
    player.armadura = armadura
    return player

def update_player(id_player, gold, level, xp):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE players 
        SET gold = %s, level = %s, xp = %s 
        WHERE id = %s
    """, (gold, level, xp, id_player))

    conexao.commit()
    cursor.close()
    conexao.close()

def delete_player(id_player):
    player = buscar_player(id_player)
    if player is None:
        print("Player não encontrado, nada foi deletado.")
        return

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM players WHERE id = %s", (id_player,))
    conexao.commit()
    cursor.close()
    conexao.close()
    print(f"{player.nome} foi deletado.")

def salvar_player(player, player_id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE players SET
            hp = %s, hp_maximo = %s, mana = %s, gold = %s, xp = %s,
            level = %s, ataque_base = %s, ataque = %s, armadura = %s, armadura_base = %s
        WHERE id = %s
    """, (player.hp, player.hp_maximo, player.mana, player.gold, player.xp,
          player.level, player.ataque_base, player.ataque, player.armadura, player.armadura_base,
          player_id))

    conexao.commit()
    cursor.close()
    conexao.close()