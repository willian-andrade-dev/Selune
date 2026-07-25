import os
from Database.shop_repository import (
    listar_itens_loja,
    comprar_item,
    vender_item,
    listar_inventario_vendavel,
)
from Entities.player import Player

PAGE_SIZE = 15
CATEGORIAS_COMPRAVEIS = ["Arma", "Armadura", "Consumivel", "Acessorio"]


class Shop:
    def __init__(self, player: Player, player_id: int):
        self.player = player
        self.player_id = player_id

    def _clear(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def _pausar(self) -> None:
        input("\nPressione Enter para continuar...")

    def _confirmar(self, mensagem: str) -> bool:
        resposta = input(f"{mensagem} (s/n): ").strip().lower()
        return resposta == "s"

    def _ler_quantidade(self, maximo: int = None) -> int:
        entrada = input("Quantidade (padrão 1): ").strip()
        if not entrada:
            return 1
        try:
            valor = int(entrada)
        except ValueError:
            return 1
        if valor <= 0:
            return 1
        if maximo is not None and valor > maximo:
            return maximo
        return valor

    def _escolher_categoria(self):
        self._clear()
        print("==== O QUE VOCÊ QUER COMPRAR? ====")
        for i, categoria in enumerate(CATEGORIAS_COMPRAVEIS, start=1):
            print(f"{i} - {categoria}")
        print("0 - Voltar")

        escolha = input("Escolha uma categoria: ").strip()
        if escolha == "0":
            return None
        try:
            indice = int(escolha) - 1
            if 0 <= indice < len(CATEGORIAS_COMPRAVEIS):
                return CATEGORIAS_COMPRAVEIS[indice]
        except ValueError:
            pass

        print("Opção inválida.")
        self._pausar()
        return self._escolher_categoria()

    def _filtrar_por_nivel(self, itens: list) -> list:
        entrada = input("Filtrar por nível, ex: 1-20 (Enter para ver todos): ").strip()
        if not entrada:
            return itens
        try:
            minimo_str, maximo_str = entrada.split("-")
            minimo, maximo = int(minimo_str), int(maximo_str)
        except ValueError:
            print("Formato inválido, mostrando todos os itens.")
            self._pausar()
            return itens
        return [item for item in itens if minimo <= item["nivel_requerido"] <= maximo]

    def _paginar_e_escolher(self, itens: list, titulo: str, preco_campo: str):
        if not itens:
            print("Nenhum item encontrado.")
            self._pausar()
            return None

        pagina = 0
        total_paginas = max(1, (len(itens) + PAGE_SIZE - 1) // PAGE_SIZE)

        while True:
            self._clear()
            inicio = pagina * PAGE_SIZE
            pagina_itens = itens[inicio:inicio + PAGE_SIZE]

            print(f"==== {titulo} (página {pagina + 1}/{total_paginas}) ====")
            print(f"Seu gold: {self.player.gold}\n")
            for i, item in enumerate(pagina_itens, start=1):
                preco = item[preco_campo]
                print(f"{i:>2} - {item['nome']} (nível {item['nivel_requerido']}, {item['raridade']}) - {preco} gold")

            print("\nN - Próxima página | P - Página anterior | 0 - Voltar")
            escolha = input("Escolha um item: ").strip().upper()

            if escolha == "0":
                return None
            elif escolha == "N":
                pagina = min(pagina + 1, total_paginas - 1)
            elif escolha == "P":
                pagina = max(pagina - 1, 0)
            else:
                try:
                    indice = int(escolha) - 1
                    if 0 <= indice < len(pagina_itens):
                        return pagina_itens[indice]
                except ValueError:
                    pass
                print("Opção inválida.")
                self._pausar()

    def _comprar(self) -> None:
        categoria = self._escolher_categoria()
        if categoria is None:
            return

        self._clear()
        itens = listar_itens_loja(tipo=categoria)
        if not itens:
            print(f"Nenhum item de {categoria} disponível na loja.")
            self._pausar()
            return

        itens = self._filtrar_por_nivel(itens)
        item = self._paginar_e_escolher(itens, f"LOJA - {categoria.upper()}", "preco_compra")
        if item is None:
            return

        self._clear()
        print(f"{item['nome']} (nível {item['nivel_requerido']}, {item['raridade']}) - {item['preco_compra']} gold/un")
        quantidade = self._ler_quantidade()
        total = item["preco_compra"] * quantidade

        if not self._confirmar(f"Confirma a compra de {quantidade}x {item['nome']} por {total} gold?"):
            print("Compra cancelada.")
            self._pausar()
            return

        sucesso, mensagem, gold_gasto = comprar_item(self.player_id, item["item_id"], quantidade)
        print(mensagem)
        if sucesso:
            self.player.gold -= gold_gasto
        self._pausar()

    def _vender(self) -> None:
        self._clear()
        itens = listar_inventario_vendavel(self.player_id)

        if not itens:
            print("Seu inventário está vazio.")
            self._pausar()
            return

        print("==== SEU INVENTÁRIO ====\n")
        for i, item in enumerate(itens, start=1):
            print(f"{i:>2} - {item['nome']} x{item['quantidade']} ({item['tipo']}, {item['raridade']}) "
                  f"- {item['preco_venda']} gold/un")
        print("\n0 - Voltar")

        escolha = input("\nEscolha o item que deseja vender: ").strip()
        if escolha == "0":
            return

        try:
            indice = int(escolha) - 1
            if not (0 <= indice < len(itens)):
                raise ValueError
        except ValueError:
            print("Opção inválida.")
            self._pausar()
            return

        item = itens[indice]
        quantidade = self._ler_quantidade(maximo=item["quantidade"])
        total = item["preco_venda"] * quantidade

        if not self._confirmar(f"Confirma a venda de {quantidade}x {item['nome']} por {total} gold?"):
            print("Venda cancelada.")
            self._pausar()
            return

        sucesso, mensagem, gold_ganho = vender_item(self.player_id, item["item_id"], quantidade)
        print(mensagem)
        if sucesso:
            self.player.gold += gold_ganho
        self._pausar()

    def abrir(self: "Shop") -> None:
        while True:
            self._clear()
            print("==== LOJA ====")
            print(f"Seu gold: {self.player.gold}\n")
            print("1 - Comprar item")
            print("2 - Vender item")
            print("3 - Sair da loja")

            escolha = input("Escolha uma opção: ").strip()

            if escolha == "1":
                self._comprar()
            elif escolha == "2":
                self._vender()
            elif escolha == "3":
                break
            else:
                print("Opção inválida.")
                self._pausar()