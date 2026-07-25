from Entities.item import Item, Consumivel, Weapon, Armadura, Acessorio
from collections import Counter

class Inventory:
    def __init__(self: 'Inventory') -> None:
        self.itens = []

    def adicionar_item(self: 'Inventory', item: 'Item') -> None:
        self.itens.append(item)

    def mostrar_inventario(self: 'Inventory') -> None:
        if not self.itens:
            print("Seu inventário está vazio")
            return

        print("==== INVENTÁRIO ===")
        contagem = Counter(item.nome for item in self.itens)
        ja_mostrados = set()

        for item in self.itens:
            if item.nome in ja_mostrados:
                continue
            ja_mostrados.add(item.nome)
            quantidade = contagem[item.nome]
            print(f"{item} x{quantidade}")

    def listar_pocoes(self: 'Inventory') -> list:
        """Retorna lista de tuplas (item, quantidade) únicas de poções de cura disponíveis."""
        contagem = Counter(item.nome for item in self.itens)
        nomes_vistos = set()
        pocoes = []

        for item in self.itens:
            if isinstance(item, Consumivel) and item.eh_pocao_cura() and item.nome not in nomes_vistos:
                nomes_vistos.add(item.nome)
                pocoes.append((item, contagem[item.nome]))

        return pocoes

    def listar_equipaveis(self: 'Inventory') -> list:
        """Retorna lista de tuplas (item, quantidade) únicas de armas, armaduras e acessórios."""
        contagem = Counter(item.nome for item in self.itens)
        nomes_vistos = set()
        equipaveis = []

        for item in self.itens:
            eh_equipavel = isinstance(item, (Weapon, Armadura, Acessorio))
            if eh_equipavel and item.nome not in nomes_vistos:
                nomes_vistos.add(item.nome)
                equipaveis.append((item, contagem[item.nome]))

        return equipaveis

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