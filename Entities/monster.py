from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from Entities.player import Player
    from Entities.item import Item

class Monstro:
    def __init__(self, nome: str, hp: int, loot: Optional['Item'], ataque: int, xp: int, ouro: int) -> None:
        self.nome = nome
        self.hp = hp
        self.loot = loot
        self.ataque = ataque
        self.xp = xp
        self.ouro = ouro

    def atacar(self: 'Monstro', player: 'Player') -> None:
        player.hp = player.hp - self.ataque
        print(f"Player HP: {player.hp}")
