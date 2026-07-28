from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Entities.item import Item
    from Entities.player import Player


class Recipe:
    def __init__(self, id: int, item_resultado: 'Item', quantidade_produzida: int,
                 nivel_crafting_minimo: int, tipo_estacao: str, ingredientes: list) -> None:
        self.id = id
        self.item_resultado = item_resultado
        self.quantidade_produzida = quantidade_produzida
        self.nivel_crafting_minimo = nivel_crafting_minimo
        self.tipo_estacao = tipo_estacao
        self.ingredientes = ingredientes  # lista de {"item": Item, "quantidade": int}

    def __str__(self):
        return (f"Receita de {self.item_resultado.nome} "
                f"(nível {self.nivel_crafting_minimo}, estação: {self.tipo_estacao})")

    def nivel_suficiente(self, player: 'Player') -> bool:
        """Checa só o nível de crafting mínimo. Ingredientes e estação disponível
        são responsabilidade do Systems/crafting.py, não da receita em si."""
        if player.crafting_skill.nivel < self.nivel_crafting_minimo:
            print(f"Você precisa de nível de crafting {self.nivel_crafting_minimo} para "
                  f"{self.item_resultado.nome} (seu nível: {player.crafting_skill.nivel}).")
            return False
        return True