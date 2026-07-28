from typing import Optional
from Database.connection import conectar
from Entities.player import Player
from Database.equipment_repository import buscar_equipamento
from Entities.crafting_skill import CraftingSkill
from Database.crafting_skill_repository import criar_progresso_crafting, carregar_crafting_skill, atualizar_crafting_skill

def criar_player(nome: str, hp: int, hp_maximo: int, mana: int, gold: int, xp: int, xp_para_upar: int,
                  level: int, ataque_base: int, ataque: int, armadura: int, armadura_base: int,
                  classe_id: int) -> int:
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO players (nome, hp, hp_maximo, mana, gold, xp, xp_para_upar, level, ataque_base, ataque, armadura, armadura_base, classe_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (nome, hp, hp_maximo, mana, gold, xp, xp_para_upar, level, ataque_base, ataque, armadura, armadura_base, classe_id))

    player_id = cursor.fetchone()[0]
    conexao.commit()
    cursor.close()
    conexao.close()
    criar_progresso_crafting(player_id)
    return player_id

def buscar_player(id_player: int, itens: dict = None) -> Optional[Player]:
    conexao = conectar()
    cursor = conexao.cursor()

    # lista explicita de colunas (em vez de SELECT *) pra nao quebrar de novo
    # toda vez que uma coluna nova for adicionada na tabela via ALTER TABLE
    cursor.execute("""
        SELECT id, nome, hp, hp_maximo, mana, gold, xp, xp_para_upar, level,
               ataque_base, ataque, armadura, armadura_base, classe_id, gold_banco
        FROM players WHERE id = %s
    """, (id_player,))
    linha = cursor.fetchone()

    if linha is None:
        cursor.close()
        conexao.close()
        return None

    (id, nome, hp, hp_maximo, mana, gold, xp, xp_para_upar, level,
     ataque_base, ataque, armadura, armadura_base, classe_id, gold_banco) = linha

    cursor.execute("""
    SELECT hp_regen_base, hp_regen_por_nivel, mana_regen_base, mana_regen_por_nivel
    FROM classes WHERE id = %s
    """, (classe_id,))
    regen = cursor.fetchone()
    if regen:
        hp_regen_base, hp_regen_por_nivel, mana_regen_base, mana_regen_por_nivel = (float(x) for x in regen)
    else:
        hp_regen_base = hp_regen_por_nivel = mana_regen_base = mana_regen_por_nivel = 0.0

    player = Player(nome, hp, mana, gold, xp, level, ataque_base, armadura_base, classe_id,
                     hp_regen_base, hp_regen_por_nivel, mana_regen_base, mana_regen_por_nivel)
    player.id = id
    player.hp_maximo = hp_maximo
    player.xp_para_upar = xp_para_upar
    player.ataque = ataque
    player.armadura = armadura
    player.gold_banco = gold_banco

    if itens is not None:
        equipados = buscar_equipamento(id)
        if "arma" in equipados:
            player.equipamento.equipar_arma(itens[equipados["arma"]])
        if "armadura" in equipados:
            player.equipamento.equipar_armadura(itens[equipados["armadura"]])
        for slot in ("Anel", "Colar", "Amuleto", "Brinco"):
            if slot in equipados:
                player.equipamento.equipar_acessorio(itens[equipados[slot]])
        if equipados:
            player.atualizar_status()

    crafting_data = carregar_crafting_skill(id)
    player.crafting_skill = CraftingSkill(crafting_data["nivel"], crafting_data["xp"])
    return player

def update_player(id_player: int, gold: int, level: int, xp: int) -> None:
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

def delete_player(id_player: int) -> None:
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

def salvar_player(player: Player, player_id: int) -> None:
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE players SET
            hp = %s, hp_maximo = %s, mana = %s, gold = %s, xp = %s,
            level = %s, ataque_base = %s, ataque = %s, armadura = %s, armadura_base = %s,
            gold_banco = %s
        WHERE id = %s
    """, (player.hp, player.hp_maximo, player.mana, player.gold, player.xp,
          player.level, player.ataque_base, player.ataque, player.armadura, player.armadura_base, player.gold_banco,
          player_id))

    conexao.commit()
    cursor.close()
    conexao.close()

    atualizar_crafting_skill(player_id, player.crafting_skill.nivel, player.crafting_skill.xp)