import time

from Database.combat_log_repository import registrar_combate
from Database.inventory_repository import adicionar_item_inventario
from Systems.combat_base import CombatBase


class Combat(CombatBase):
    FUGA_CHANCE = 0.5

    def __init__(self, player, monstro, localizacao, habilidades):
        super().__init__(player, localizacao, habilidades)
        self.monstro = monstro

    def _escolher_alvo(self):
        return self.monstro  # 1v1: alvo é sempre o único monstro

    def start(self) -> None:
        inicio = time.time()
        print(f"Um {self.monstro.nome} apareceu!")

        while self.player.hp > 0 and self.monstro.hp > 0:
            print(f"\n{self.player.nome} HP: {self.player.hp}/{self.player.hp_maximo}")
            print(f"{self.monstro.nome} HP: {self.monstro.hp}")
            print("1 - Atacar")
            print("2 - Usar poção")
            print("3 - Usar habilidade")
            print("4 - Fugir")
            escolha = self._ler_opcao(1, 4)

            if escolha == 1:
                self.player.atacar(self.monstro)
                if self.monstro.hp <= 0:
                    break

            elif escolha == 2:
                if not self.player.usar_pocao(self._ler_opcao):
                    continue

            elif escolha == 3:
                if not self._usar_habilidade_turno():
                    continue

            else:
                if self._tentar_fugir():
                    print(f"{self.player.nome} escapou são e salvo, sem ganhar XP nem ouro desta vez.")
                    return

            self.player.atualizar_buffs_turno()
            self.player.atualizar_cooldowns_turno()
            self.player.atualizar_regen_turno()

            if self.monstro.hp <= 0:
                break

            self.monstro.atacar(self.player)

        duracao = int((time.time() - inicio) * 1000)
        venceu = self.player.hp > 0

        if not venceu:
            print(f"{self.player.nome} foi derrotado...")
            self.player.hp = max(self.player.hp_maximo // 2, 1)
            print(f"Você acordou em segurança com {self.player.hp}/{self.player.hp_maximo} de HP.")
            registrar_combate(self.player.id, self.monstro.id, 0, 0, False, duracao)
            return

        xp_ganho = int(self.monstro.xp * (1 + self.player.bonus_xp / 100))
        ouro_ganho = int(self.monstro.ouro * (1 + self.player.bonus_ouro / 100))
        self.player.xp += xp_ganho
        self.player.subir_nivel()
        self.player.gold += ouro_ganho

        itens_dropados = self.monstro.sortear_drops()
        for item in itens_dropados:
            self.player.inventario.adicionar_item(item)
            adicionar_item_inventario(self.player.id, item.id, 1)

        registrar_combate(self.player.id, self.monstro.id, xp_ganho, ouro_ganho, True, duracao)

        if itens_dropados:
            nomes = ", ".join(item.nome for item in itens_dropados)
            print(f"Você derrotou {self.monstro.nome}! Ganhou {xp_ganho} de XP, {ouro_ganho} de Ouro e dropou: {nomes}")
        else:
            print(f"Você derrotou {self.monstro.nome}! Ganhou {xp_ganho} de XP e {ouro_ganho} de Ouro")