import random
from abc import ABC, abstractmethod


class CombatBase(ABC):
    FUGA_CHANCE = 0.5  # sobrescrito por subclasses que precisem de outro valor

    def __init__(self, player, localizacao, habilidades):
        self.player = player
        self.localizacao = localizacao
        self.habilidades = habilidades
        self.player.cooldowns_habilidades = {}

    def _ler_opcao(self, minimo: int, maximo: int) -> int:
        while True:
            try:
                valor = int(input("Escolha uma opção: "))
                if minimo <= valor <= maximo:
                    return valor
                print(f"Digite um número entre {minimo} e {maximo}.")
            except ValueError:
                print("Digite apenas números.")

    def _tentar_fugir(self) -> bool:
        if random.random() < self.FUGA_CHANCE:
            print(f"{self.player.nome} fugiu do combate!")
            return True
        print(f"{self.player.nome} tentou fugir, mas não conseguiu!")
        return False

    def _usar_habilidade_turno(self) -> bool:
        disponiveis = self.player.habilidades_disponiveis(self.habilidades)
        if not disponiveis:
            print("Você ainda não tem nenhuma habilidade disponível.")
            return False

        print("\n=== HABILIDADES ===")
        for i, h in enumerate(disponiveis, start=1):
            cooldown = self.player.cooldowns_habilidades.get(h.id, 0)
            status = f" [cooldown: {cooldown}]" if cooldown > 0 else ""
            print(f"{i} - {h.nome} (custo: {h.custo_mana} mana){status} - {h.descricao}")
        print(f"{len(disponiveis) + 1} - Cancelar")

        escolha = self._ler_opcao(1, len(disponiveis) + 1)
        if escolha == len(disponiveis) + 1:
            return False

        habilidade = disponiveis[escolha - 1]
        alvo = self._escolher_alvo()
        return habilidade.usar(self.player, alvo)

    @abstractmethod
    def _escolher_alvo(self):
        """Retorna o monstro que deve receber o próximo ataque/habilidade."""
        raise NotImplementedError