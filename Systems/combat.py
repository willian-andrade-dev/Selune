import time
import random
from Database.combat_log_repository import registrar_combate
from Database.inventory_repository import adicionar_item_inventario
from Entities.monster import Monstro
from World.location import Localização
from Entities.player import Player

class Combat:
    FUGA_CHANCE = 0.5

    def __init__(self, player: Player, monstro: Monstro, localizacao: Localização, habilidades: list):
        self.player = player
        self.monstro = monstro
        self.localizacao = localizacao
        self.habilidades = habilidades
        self.fugiu = False

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
        """Retorna True se a fuga teve sucesso (combate encerra), False se falhou (turno consumido)."""
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
        return habilidade.usar(self.player, self.monstro)

    def _curar_turno(self) -> bool:
        """Retorna True se o turno foi consumido (poção usada), False se cancelado/sem poções."""
        pocoes = self.player.inventario.listar_pocoes_cura()

        if not pocoes:
            print("Você não tem nenhuma poção de cura no inventário!")
            return False

        print("\n=== POÇÕES DISPONÍVEIS ===")
        for i, (item, quantidade) in enumerate(pocoes, start=1):
            print(f"{i} - {item.nome} ({item.descricao_cura()}) x{quantidade}")
        print(f"{len(pocoes) + 1} - Cancelar")

        escolha = self._ler_opcao(1, len(pocoes) + 1)
        if escolha == len(pocoes) + 1:
            return False

        item_escolhido, _ = pocoes[escolha - 1]
        item_escolhido.use(self.player)
        return True

    def start(self: 'Combat') -> None:
        inicio = time.time()
        print(f"Você encontrou um {self.monstro.nome} em {self.localizacao.nome}!")

        while self.player.hp > 0 and self.monstro.hp > 0:
            print(f"\n{self.player.nome} HP: {self.player.hp}/{self.player.hp_maximo}  |  "
                  f"{self.monstro.nome} HP: {self.monstro.hp}")
            print("1 - Atacar")
            print("2 - Se curar")
            print("3 - Usar habilidade")
            print("4 - Fugir")
            escolha = self._ler_opcao(1, 4)

            if escolha == 1:
                self.player.atacar(self.monstro)
            elif escolha == 2:
                turno_usado = self.player.usar_pocao_cura(self._ler_opcao)
                if not turno_usado:
                    continue
            elif escolha == 3:
                turno_usado = self._usar_habilidade_turno()
                if not turno_usado:
                    continue
            else:
                if self._tentar_fugir():
                    self.fugiu = True
                    break

            if self.monstro.hp <= 0:
                break

            self.monstro.atacar(self.player)
            self.player.atualizar_buffs_turno()
            self.player.atualizar_cooldowns_turno()

        duracao = int((time.time() - inicio) * 1000)

        if self.fugiu:
            print(f"{self.player.nome} escapou são e salvo, sem ganhar XP nem ouro desta vez.")
            return  # sem registrar combate, sem penalidade, sem recompensa

        venceu = self.player.hp > 0

        if not venceu:
            print(f"{self.player.nome} foi derrotado...")
            self.player.hp = max(self.player.hp_maximo // 2, 1)
            print(f"Você acordou em segurança com {self.player.hp}/{self.player.hp_maximo} de HP.")
            registrar_combate(self.player.id, self.monstro.id, 0, 0, False, duracao)
        else:
            print(f"Você derrotou {self.monstro.nome}!")
            self.player.xp += self.monstro.xp
            self.player.subir_nivel()
            self.player.gold += self.monstro.ouro

            itens_dropados = self.monstro.sortear_drops()
            for item in itens_dropados:
                self.player.inventario.adicionar_item(item)
                adicionar_item_inventario(self.player.id, item.id, 1)

            if itens_dropados:
                nomes = ", ".join(item.nome for item in itens_dropados)
                print(f"Você ganhou {self.monstro.xp} de XP, {self.monstro.ouro} peças de Ouro "
                      f"e dropou: {nomes}")
            else:
                print(f"Você ganhou {self.monstro.xp} de XP, {self.monstro.ouro} peças de Ouro")

            registrar_combate(self.player.id, self.monstro.id, self.monstro.xp, self.monstro.ouro, True, duracao)