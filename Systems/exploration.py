import random
import copy

class Exploration:
    def __init__(self, localizacoes: list, monstros: list) -> None:
        self.localizacoes = localizacoes
        self.monstros = monstros

    def localizacoes_ordenadas(self) -> list:
        return sorted(self.localizacoes, key=lambda loc: loc.dificuldade)

    def monstros_da_localizacao(self, localizacao) -> list:
        return [m for m in self.monstros if localizacao.id in m.location_ids]

    def sortear_monstro(self, localizacao):
        disponiveis = self.monstros_da_localizacao(localizacao)
        if not disponiveis:
            return None
        return copy.deepcopy(random.choice(disponiveis))