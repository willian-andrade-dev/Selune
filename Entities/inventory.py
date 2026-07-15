from Entities.item import Item
from collections import Counter

class Inventory:
    def __init__(self: 'Inventory') -> None:
        self.itens = []

    def adicionar_item(self: 'Inventory', item: 'Item') -> None:
        self.itens.append(item)

    def mostrar_inventario(self: 'Inventory') -> None:
        if not self.itens:
            print("Seu inventário está vazio")
        else:
            print("==== INVENTÁRIO ===")
            contagem = Counter(item.nome for item in self.itens)
            ja_mostrados = set()

            for item in self.itens:
                if item.nome in ja_mostrados:
                    continue
                ja_mostrados.add(item.nome)
                quantidade = contagem[item.nome]
                print(f"{item} x{quantidade}")

    def procurar_item(self: 'Inventory', nome: str) -> 'Item':
        for item in self.itens:
            if item.nome == nome:
                return item
        return None

    def remover_item(self: 'Inventory', item: str) -> None:
        if item not in self.itens:
            print("Item não encontrado no seu inventário")
        else:
            self.itens.remove(item)
