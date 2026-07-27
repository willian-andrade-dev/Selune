import time
import random

from Database.combat_log_repository import registrar_combate
from Database.inventory_repository import adicionar_item_inventario
from Systems.combat_base import CombatBase


class GroupCombat(CombatBase):
    FUGA_CHANCE = 0.3  # fugir de 2-3 monstros é mais arriscado que de 1

    def __init__(self, player, monstros: list, localizacao, habilidades):
        super().__init__(player, localizacao, habilidades)
        self.monstros = monstros
        self.fugiu = False

    def _monstros_vivos(self) -> list:
        return [m for m in self.monstros if m.hp > 0]

    def _mostrar_status(self) -> None:
        print(f"\n{self.player.nome} HP: {self.player.hp}/{self.player.hp_maximo}")
        for i, m in enumerate(self._monstros_vivos(), start=1):
            print(f"  {i} - {m.nome} HP: {m.hp}")

    def _escolher_alvo(self):
        vivos = self._monstros_vivos()
        if len(vivos) == 1:
            return vivos[0]

        print("\nEscolha o alvo:")
        for i, m in enumerate(vivos, start=1):
            print(f"{i} - {m.nome} (HP: {m.hp})")
        escolha = self._ler_opcao(1, len(vivos))
        return vivos[escolha - 1]

    def start(self) -> None:
        inicio = time.time()
        nomes_iniciais = ", ".join(m.nome for m in self.monstros)
        print(f"Você encontrou um grupo de monstros em {self.localizacao.nome}: {nomes_iniciais}!")

        while self.player.hp > 0 and self._monstros_vivos():
            self._mostrar_status()
            print("1 - Atacar")
            print("2 - Usar poção")
            print("3 - Usar habilidade")
            print("4 - Fugir")
            escolha = self._ler_opcao(1, 4)

            if escolha == 1:
                alvo = self._escolher_alvo()
                self.player.atacar(alvo)
                if alvo.hp <= 0:
                    print(f"{alvo.nome} foi derrotado!")

            elif escolha == 2:
                if not self.player.usar_pocao(self._ler_opcao):
                    continue

            elif escolha == 3:
                if not self._usar_habilidade_turno():
                    continue

            else:
                if self._tentar_fugir():
                    self.fugiu = True
                    break

            self.player.atualizar_buffs_turno()
            self.player.atualizar_cooldowns_turno()
            self.player.atualizar_regen_turno()

            vivos = self._monstros_vivos()
            if not vivos:
                break

            for monstro in vivos:
                monstro.atacar(self.player)
                if self.player.hp <= 0:
                    break

        duracao = int((time.time() - inicio) * 1000)

        if self.fugiu:
            print(f"{self.player.nome} escapou são e salvo, sem ganhar XP nem ouro desta vez.")
            return

        venceu = self.player.hp > 0

        if not venceu:
            print(f"{self.player.nome} foi derrotado...")
            self.player.hp = max(self.player.hp_maximo // 2, 1)
            print(f"Você acordou em segurança com {self.player.hp}/{self.player.hp_maximo} de HP.")
            for monstro in self.monstros:
                registrar_combate(self.player.id, monstro.id, 0, 0, False, duracao)
            return

        print(f"Você derrotou o grupo: {nomes_iniciais}!")

        xp_total = 0
        ouro_total = 0
        drops_totais = []

        for monstro in self.monstros:
            xp_ganho = int(monstro.xp * (1 + self.player.bonus_xp / 100))
            ouro_ganho = int(monstro.ouro * (1 + self.player.bonus_ouro / 100))
            xp_total += xp_ganho
            ouro_total += ouro_ganho

            itens_dropados = monstro.sortear_drops()
            for item in itens_dropados:
                self.player.inventario.adicionar_item(item)
                adicionar_item_inventario(self.player.id, item.id, 1)
                drops_totais.append(item)

            registrar_combate(self.player.id, monstro.id, xp_ganho, ouro_ganho, True, duracao)

        self.player.xp += xp_total
        self.player.subir_nivel()
        self.player.gold += ouro_total

        if drops_totais:
            nomes_drops = ", ".join(item.nome for item in drops_totais)
            print(f"Você ganhou {xp_total} de XP, {ouro_total} peças de Ouro e dropou: {nomes_drops}")
        else:
            print(f"Você ganhou {xp_total} de XP, {ouro_total} peças de Ouro")