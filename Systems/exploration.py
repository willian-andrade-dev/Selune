import random
import copy

from Systems.monster_utils import monstros_da_localizacao


class Exploration:
    def __init__(self, localizacoes: list, monstros: list) -> None:
        self.localizacoes = localizacoes
        self.monstros = monstros

    def localizacoes_ordenadas(self) -> list:
        return sorted(self.localizacoes, key=lambda loc: loc.dificuldade)

    def sortear_monstro(self, localizacao):
        disponiveis = monstros_da_localizacao(self.monstros, localizacao)
        if not disponiveis:
            return None
        return copy.deepcopy(random.choice(disponiveis))