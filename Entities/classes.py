from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Entities.player import Player

class Classe:
    def __init__(self, id: int, nome: str, descricao: str,
                 hp_base: int, mana_base: int, ataque_base: int, armadura_base: int) -> None:
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.hp_base = hp_base
        self.mana_base = mana_base
        self.ataque_base = ataque_base
        self.armadura_base = armadura_base


class Habilidade:
    def __init__(self, id: int, classe_id: int, nome: str, descricao: str,
                 nivel_requerido: int, custo_mana: int, tipo: str, valor: int,
                 duracao_turnos: int = 0) -> None:
        self.id = id
        self.classe_id = classe_id
        self.nome = nome
        self.descricao = descricao
        self.nivel_requerido = nivel_requerido
        self.custo_mana = custo_mana
        self.tipo = tipo
        self.valor = valor
        self.duracao_turnos = duracao_turnos

    def usar(self, player: 'Player', monstro=None) -> None:
        if player.mana < self.custo_mana:
            print(f"Mana insuficiente para usar {self.nome} (precisa de {self.custo_mana}, tem {player.mana}).")
            return

        player.mana -= self.custo_mana

        if self.tipo == "dano" and monstro is not None:
            monstro.hp -= self.valor
            print(f"{player.nome} usou {self.nome} em {monstro.nome}, causando {self.valor} de dano!")

        elif self.tipo == "cura":
            hp_antes = player.hp
            player.hp = min(player.hp + self.valor, player.hp_maximo)
            curado = player.hp - hp_antes
            print(f"{player.nome} usou {self.nome}, curando {curado} de HP. HP atual: {player.hp}/{player.hp_maximo}")

        elif self.tipo in ("buff_ataque", "buff_armadura"):
            player.aplicar_buff(self.tipo, self.valor, self.duracao_turnos)
            print(f"{player.nome} usou {self.nome}! Efeito ativo por {self.duracao_turnos} turnos.")

        else:
            print(f"{self.nome}: tipo de efeito desconhecido.")