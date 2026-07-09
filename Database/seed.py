from Database.item_repository import criar_item
from Database.location_repository import criar_localizacao
from Database.monster_repository import criar_monstro

def popular_items():
    criar_item("Espada Enferrujada", "Arma", 5, "Uma simples espada enferrujada", dano=5)
    criar_item("Carne Podre", "Loot", 2, "Drop comum de um Zumbi")
    criar_item("Poção de Cura", "Consumivel", 20, "Recupera 10 de HP", funcao="Recuperar vida")
    criar_item("Osso", "Loot", 4, "Drop comum de um Esqueleto")
    criar_item("Espada de Ferro", "Arma", 30, "Espada utilizada por soldados imperiais", dano=15)
    criar_item("Armadura de Adamantium", "Armadura", 80, "Uma armadura vestida pelos mais poderosos", armadura=30)
    criar_item("Couro", "Loot", 10, "Couro simples, útil para criação de armaduras básicas")
    criar_item("Club", "Arma", 15, "Um porrete dropado de uma criatura imensa", dano=10)
    print("Items populados!")

def popular_localizacoes():
    criar_localizacao("Planices de Norteria", 1, "Norteria")
    criar_localizacao("Floresta da Escuridão", 2, "Arredores de Norteria")
    criar_localizacao("Ruinas de Neferia", 3, "Sul de Norteria")
    print("Localizações populadas!")

def popular_monstros():
    criar_monstro("Goblin", 15, loot_item_id=1, ataque=7, xp=10, ouro=5, location_ids=[1])
    criar_monstro("Orc", 30, loot_item_id=8, ataque=18, xp=25, ouro=15, location_ids=[1, 3])
    criar_monstro("Esqueleto", 12, loot_item_id=4, ataque=5, xp=8, ouro=4, location_ids=[3])
    criar_monstro("Zumbi", 20, loot_item_id=2, ataque=6, xp=12, ouro=6, location_ids=[2, 3])
    criar_monstro("Javali", 20, loot_item_id=7, ataque=15, xp=15, ouro=8, location_ids=[1, 2])
    print("Monstros populados!")

if __name__ == "__main__":
    popular_items()
    popular_localizacoes()
    popular_monstros()

