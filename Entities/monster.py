import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Entities.player import Player
    from Entities.item import Item


class Monstro:
    def __init__(self, nome: str, hp: int, ataque: int, xp: int, ouro: int) -> None:
        self.id = None
        self.nome = nome
        self.hp = hp
        self.ataque = ataque
        self.xp = xp
        self.ouro = ouro
        self.drops = []  # lista de tuplas (Item, chance_drop 0-100), populada pelo monster_repository

    def atacar(self, player):
        dano_reduzido = max(self.ataque - player.armadura, 1)
        player.hp = player.hp - dano_reduzido
        print(f"Player HP: {player.hp}")

    def sortear_drops(self) -> list:
        """Rola cada drop possível de forma independente contra sua chance (%).
        Retorna a lista de itens que efetivamente dropou (pode ser vazia)."""
        itens_dropados = []
        for item, chance in self.drops:
            if random.uniform(0, 100) <= chance:
                itens_dropados.append(item)
        return itens_dropados