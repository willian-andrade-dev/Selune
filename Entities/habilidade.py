from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Entities.player import Player

class Habilidade:
    def __init__(self, id: int, classe_id: int, nome: str, descricao: str,
                 nivel_requerido: int, custo_mana: int, tipo: str, valor: int,
                 duracao_turnos: int = 0, cooldown_turnos: int = 0) -> None:
        self.id = id
        self.classe_id = classe_id
        self.nome = nome
        self.descricao = descricao
        self.nivel_requerido = nivel_requerido
        self.custo_mana = custo_mana
        self.tipo = tipo
        self.valor = valor
        self.duracao_turnos = duracao_turnos
        self.cooldown_turnos = cooldown_turnos

    def usar(self, player: 'Player', monstro=None) -> bool:
        # cooldowns_habilidades guarda turnos RESTANTES (não turno absoluto) —
        # reseta sozinho a cada novo Combat, já que o dict é zerado no início dele.
        turnos_restantes = player.cooldowns_habilidades.get(self.id, 0)
        if turnos_restantes > 0:
            print(f"{self.nome} está em cooldown! Faltam {turnos_restantes} turno(s).")
            return False

        if player.mana < self.custo_mana:
            print(f"Mana insuficiente para usar {self.nome} (precisa de {self.custo_mana}, tem {player.mana}).")
            return False

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
            return False

        if self.cooldown_turnos > 0:
            player.cooldowns_habilidades[self.id] = self.cooldown_turnos

        return True