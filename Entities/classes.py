from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Entities.player import Player

class Classe:
    def __init__(self, id: int, nome: str, descricao: str,
                 hp_base: int, mana_base: int, ataque_base: int, armadura_base: int,
                 hp_regen_base: float = 0, hp_regen_por_nivel: float = 0,
                 mana_regen_base: float = 0, mana_regen_por_nivel: float = 0) -> None:
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.hp_base = hp_base
        self.mana_base = mana_base
        self.ataque_base = ataque_base
        self.armadura_base = armadura_base
        self.hp_regen_base = hp_regen_base
        self.hp_regen_por_nivel = hp_regen_por_nivel
        self.mana_regen_base = mana_regen_base
        self.mana_regen_por_nivel = mana_regen_por_nivel

