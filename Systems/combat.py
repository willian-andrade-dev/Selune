from Database.inventory_repository import adicionar_item_inventario

class Combat:
    def __init__(self, player, monstro, localizacao):
        self.player = player
        self.monstro = monstro
        self.localizacao = localizacao


    def start(self):
        print(f"Você encontrou um {self.monstro.nome} em {self.localizacao.nome}!")

        while self.player.hp > 0 and self.monstro.hp > 0:
            self.player.Attack(self.monstro)
            if self.monstro.hp <= 0:
                break
            self.monstro.Attack(self.player)

        if self.player.hp <= 0:
            print(f"{self.player.nome} foi derrotado...")
        else:
            print(f"Você derrotou {self.monstro.nome}!")
            self.player.xp += self.monstro.xp
            self.player.level_up()
            self.player.gold += self.monstro.ouro

            if self.monstro.loot is not None:
                self.player.inventario.adicionar_item(self.monstro.loot)
                adicionar_item_inventario(self.player.id, self.monstro.loot.id, 1)
                print(f"Você ganhou {self.monstro.xp} de XP, {self.monstro.ouro} peças de Ouro e {self.monstro.loot.nome} como loot")
            else:
                print(f"Você ganhou {self.monstro.xp} de XP, {self.monstro.ouro} peças de Ouro")