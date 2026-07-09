class Inventory:
    def __init__(self):
        self.itens = []

    def adicionar_item(self, item):
        self.itens.append(item)

    def mostrar_inventario(self):
        if not self.itens:
            print("Seu inventário está vazio")
        else:
            print("==== INVENTÁRIO ===")
            for item in self.itens:
                print(item)

    def procurar_item(self, nome):
        for item in self.itens:
            if item.nome == nome:
                return item
        return None

    def remover_item(self, item):
        if item not in self.itens:
            print("Item não encontrado no seu inventário")
        else:
            self.itens.remove(item)
