from Database.inventory_repository import remover_item_inventario
from Database.equipment_repository import equipar_item
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Entities.player import Player


class Item:
    def __init__(self, nome: str, valor: int, descricao: str, nivel_requerido: int = 1, raridade: str = "Comum") -> None:
        self.id = None
        self.nome = nome
        self.valor = valor
        self.descricao = descricao
        self.nivel_requerido = nivel_requerido
        self.raridade = raridade

    def __str__(self):
        return f"{self.nome} ({self.tipo}) [{self.raridade}] - {self.descricao}"

    def pode_equipar(self: 'Item', player: 'Player') -> bool:
        """Checa se o player tem nível suficiente para equipar este item."""
        if player.level < self.nivel_requerido:
            print(f"Você precisa ser nível {self.nivel_requerido} para equipar {self.nome} "
                  f"(seu nível: {player.level}).")
            return False
        return True


class Armadura(Item):
    tipo = 'Armadura'

    def __init__(self, nome: str, valor: int, descricao: str, nivel_requerido: int, raridade: str,
                 armadura: int, efeitos: list = None) -> None:
        super().__init__(nome, valor, descricao, nivel_requerido, raridade)
        self.armadura = armadura
        self.efeitos = efeitos or []  # bônus extra (item_effects), ainda não aplicados aos stats do player

    def use(self: 'Armadura', player: 'Player') -> bool:
        if not self.pode_equipar(player):
            return False
        player.equipamento.equipar_armadura(self)
        player.atualizar_status()
        equipar_item(player.id, "armadura", self.id)
        print(f"Sua armadura atual: {player.armadura}")
        return True

class Weapon(Item):
    tipo = 'Arma'

    def __init__(self, nome: str, valor: int, descricao: str, nivel_requerido: int, raridade: str,
                 dano: int, efeitos: list = None) -> None:
        super().__init__(nome, valor, descricao, nivel_requerido, raridade)
        self.dano = dano
        self.efeitos = efeitos or []  # bônus extra (item_effects), ainda não aplicados aos stats do player

    def use(self: 'Weapon', player: 'Player') -> bool:
        if not self.pode_equipar(player):
            return False
        player.equipamento.equipar_arma(self)
        player.atualizar_status()
        equipar_item(player.id, "arma", self.id)
        print(f"Seu ataque atual: {player.ataque}")
        return True

class Consumivel(Item):
    tipo = 'Consumivel'

    # mapeia funcao -> quantidade de cura fixa
    _CURA_FIXA = {
        "curar_10": 10,
        "curar_25": 25,
        "curar_50": 50,
    }
    # mapeia funcao -> quantidade de mana fixa
    _MANA_FIXA = {
        "mana_15": 15,
        "mana_40": 40,
    }

    def __init__(self, nome: str, valor: int, descricao: str, nivel_requerido: int, raridade: str,
                 funcao: str) -> None:
        super().__init__(nome, valor, descricao, nivel_requerido, raridade)
        self.funcao = funcao

    def _consumir(self, player: 'Player') -> None:
        player.inventario.remover_item(self)
        remover_item_inventario(player.id, self.id, 1)

    def eh_pocao_cura(self) -> bool:
        return self.funcao in self._CURA_FIXA or self.funcao == "curar_total"

    def descricao_efeito(self) -> str:
        if self.funcao == "curar_total":
            return "cura toda a vida"
        return f"cura {self._CURA_FIXA[self.funcao]} HP"

    def use(self: 'Consumivel', player: 'Player') -> None:
        if self.funcao in self._CURA_FIXA:
            cura = self._CURA_FIXA[self.funcao]
            hp_antes = player.hp
            player.hp = min(player.hp + cura, player.hp_maximo)
            curado = player.hp - hp_antes
            print(f"{player.nome} usou {self.nome}, +{curado} HP. HP atual: {player.hp}/{player.hp_maximo}")
            self._consumir(player)

        elif self.funcao == "curar_total":
            player.hp = player.hp_maximo
            print(f"{player.nome} usou {self.nome} e recuperou toda a vida! HP: {player.hp}/{player.hp_maximo}")
            self._consumir(player)

        elif self.funcao in self._MANA_FIXA:
            mana = self._MANA_FIXA[self.funcao]
            player.mana += mana
            print(f"{player.nome} usou {self.nome}, +{mana} de mana. Mana atual: {player.mana}")
            self._consumir(player)

        elif self.funcao == "bonus_xp":
            bonus = 50  # valor fixo por enquanto
            player.xp += bonus
            player.subir_nivel()
            print(f"{player.nome} usou {self.nome} e ganhou {bonus} de XP extra!")
            self._consumir(player)

        elif self.funcao == "elixir_heroi":
            player.hp = player.hp_maximo
            mana_antes = player.mana
            player.mana += 100
            print(f"{player.nome} usou {self.nome}! HP e mana totalmente restaurados "
                  f"(mana: {mana_antes} -> {player.mana}).")
            self._consumir(player)

        elif self.funcao in ("buff_ataque", "buff_armadura"):
            # TODO: requer sistema de buffs temporários (com duração por combate) ainda não implementado
            print(f"{self.nome}: efeito de buff temporário ainda não implementado.")

        else:
            print(f"{self.nome}: efeito '{self.funcao}' ainda não implementado.")


class Acessorio(Item):
    tipo = 'Acessorio'

    def __init__(self, nome: str, valor: int, descricao: str, nivel_requerido: int, raridade: str,
                 subtipo: str, efeitos: list = None) -> None:
        super().__init__(nome, valor, descricao, nivel_requerido, raridade)
        self.subtipo = subtipo  # Anel, Colar, Amuleto ou Brinco
        self.efeitos = efeitos or []  # bônus extra (item_effects), ainda não aplicados aos stats do player

    def use(self: 'Acessorio', player: 'Player') -> bool:
        if not self.pode_equipar(player):
            return False
        player.equipamento.equipar_acessorio(self)
        player.atualizar_status() 
        equipar_item(player.id, self.subtipo, self.id)
        print(f"{self.nome} equipado!")
        return True

class Loot(Item):
    tipo = 'Loot'

    def __init__(self, nome: str, valor: int, descricao: str, nivel_requerido: int = 1, raridade: str = "Comum") -> None:
        super().__init__(nome, valor, descricao, nivel_requerido, raridade)