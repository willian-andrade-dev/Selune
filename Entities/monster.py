class Monstro:
    def __init__(self, nome, hp, loot, ataque, xp, ouro):
        self.nome = nome
        self.hp = hp
        self.loot = loot
        self.ataque = ataque
        self.xp = xp
        self.ouro = ouro

    def Attack(self, player):
        player.hp = player.hp - self.ataque
        print(f"Player HP: {player.hp}")
