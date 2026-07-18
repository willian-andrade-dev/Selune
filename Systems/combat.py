import time
from Database.combat_log_repository import registrar_combate
from Database.inventory_repository import adicionar_item_inventario
from Entities.monster import Monstro
from World.location import Localização
from Entities.player import Player

class Combat:
    def __init__(self, player: Player, monstro: Monstro, localizacao: Localização):
        self.player = player
        self.monstro = monstro
        self.localizacao = localizacao


    def start(self: 'Combat') -> None:
        inicio = time.time()
        print(f"Você encontrou um {self.monstro.nome} em {self.localizacao.nome}!")

        while self.player.hp > 0 and self.monstro.hp > 0:
            self.player.atacar(self.monstro)
            if self.monstro.hp <= 0:
                break
            self.monstro.atacar(self.player)

        duracao = int((time.time() - inicio) * 1000)
        venceu = self.player.hp > 0

        if not venceu:
            print(f"{self.player.nome} foi derrotado...")
            registrar_combate(self.player.id, self.monstro.id, 0, 0, False, duracao)
        else:
            print(f"Você derrotou {self.monstro.nome}!")
            self.player.xp += self.monstro.xp
            self.player.subir_nivel()
            self.player.gold += self.monstro.ouro

            if self.monstro.loot is not None:
                self.player.inventario.adicionar_item(self.monstro.loot)
                adicionar_item_inventario(self.player.id, self.monstro.loot.id, 1)
                print(f"Você ganhou {self.monstro.xp} de XP, {self.monstro.ouro} peças de Ouro e {self.monstro.loot.nome} como loot")
            else:
                print(f"Você ganhou {self.monstro.xp} de XP, {self.monstro.ouro} peças de Ouro")

            registrar_combate(self.player.id, self.monstro.id, self.monstro.xp, self.monstro.ouro, True, duracao)