

class Item:
    def __init__(self, nome, valor, descricao):
        self.id = None
        self.nome = nome
        self.valor = valor
        self.descricao = descricao

    def __str__(self):
        return f"{self.nome} ({self.tipo}) - {self.descricao}"

class Armadura(Item):
    tipo = 'Armadura'

    def __init__(self, nome, valor, descricao, armadura):
        super().__init__(nome, valor, descricao)
        self.armadura = armadura

    def use(self, player):
        player.equipamento.equipar_armadura(self)
        player.atualizar_status()
        print(f"Sua armadura atual: {player.armadura}")

class Weapon(Item):
    tipo = 'Arma'

    def __init__(self, nome, valor, descricao, dano):
        super().__init__(nome, valor, descricao)
        self.dano = dano

    def use(self, player):
        player.equipamento.equipar_arma(self)
        player.atualizar_status()
        print(f"Seu ataque atual: {player.ataque}")

class Consumivel(Item):
    tipo = 'Consumivel'

    def __init__(self, nome, valor, descricao, funcao):
        super().__init__(nome, valor, descricao)
        self.funcao = funcao

    def use(self, player):
        if self.nome != "Poção de Cura":
            print(f"Ainda em construção")
        
        else:
            player.Heal()

class Acessorio(Item):
    tipo = 'Acessorio'

    def __init__(self, nome, valor, descricao, propriedade):
        super().__init__(nome, valor, descricao)
        self.propriedade = propriedade

    def use(self, player):
        print(f"{self.nome} equipado! (efeito ainda não implementado)")


class Loot(Item):
    tipo = 'Loot'

    def __init__(self, nome, valor, descricao):
        super().__init__(nome, valor, descricao)

