from Database.inventory_repository import remover_item_inventario
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Entities.player import Player
class Item:
    def __init__(self, nome: str, valor: int, descricao: str) -> None:
        self.id = None
        self.nome = nome
        self.valor = valor
        self.descricao = descricao

    def __str__(self):
        return f"{self.nome} ({self.tipo}) - {self.descricao}"

class Armadura(Item):
    tipo = 'Armadura'

    def __init__(self, nome: str, valor: int, descricao: str, armadura: int) -> None:
        super().__init__(nome, valor, descricao)
        self.armadura = armadura

    def use(self: 'Armadura', player: 'Player') -> None:
        player.equipamento.equipar_armadura(self)
        player.atualizar_status()
        print(f"Sua armadura atual: {player.armadura}")

class Weapon(Item):
    tipo = 'Arma'

    def __init__(self, nome: str, valor: int, descricao: str, dano: int) -> None:
        super().__init__(nome, valor, descricao)
        self.dano = dano

    def use(self: 'Weapon', player: 'Player') -> None:
        player.equipamento.equipar_arma(self)
        player.atualizar_status()
        print(f"Seu ataque atual: {player.ataque}")

class Consumivel(Item):
    tipo = 'Consumivel'

    def __init__(self, nome: str, valor: int, descricao: str, funcao: str) -> None:
        super().__init__(nome, valor, descricao)
        self.funcao = funcao

    def use(self: 'Consumivel', player: 'Player') -> None:
        if self.nome != "Poção de Cura":
            print(f"Ainda em construção")
        
        else:
            player.curar()
            player.inventario.remover_item(self)
            remover_item_inventario(player.id, self.id, 1)

class Acessorio(Item):
    tipo = 'Acessorio'

    def __init__(self, nome: str, valor: int, descricao: str, propriedade: str) -> None:
        super().__init__(nome, valor, descricao)
        self.propriedade = propriedade

    def use(self: 'Acessorio', player: 'Player') -> None:
        print(f"{self.nome} equipado! (efeito ainda não implementado)")


class Loot(Item):
    tipo = 'Loot'

    def __init__(self, nome: str, valor: int, descricao: str) -> None:
        super().__init__(nome, valor, descricao)

