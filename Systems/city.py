import os
from Database.city_repository import carregar_bancadas
from Systems.bank import Bank

class CityMenu:
    def __init__(self, cidades: list, player, player_id: int, receitas_por_item: dict = None):
        self.cidades = cidades
        self.player = player
        self.player_id = player_id
        self.receitas_por_item = receitas_por_item or {}

    def _clear(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def _ler_opcao(self, minimo: int, maximo: int) -> int:
        while True:
            try:
                valor = int(input("Escolha uma opção: "))
                if minimo <= valor <= maximo:
                    return valor
                print(f"Digite um número entre {minimo} e {maximo}.")
            except ValueError:
                print("Digite apenas números.")

    def _usar_bancada(self, bancada) -> None:
        # TODO: crafting ainda não implementado — cada bancada só permite craftar
        # o tipo de item correspondente (Ferraria: Arma/Armadura, Alquimia: Consumivel,
        # Joalheria: Acessorio, Arcanismo: Pergaminho) quando as receitas existirem.
        print(f"\n[{bancada.tipo}] Sistema de crafting ainda em desenvolvimento.")
        input("\nPressione Enter para continuar...")

    def _mostrar_bancadas(self, cidade) -> None:
        while True:
            self._clear()
            bancadas = carregar_bancadas(cidade.id)

            print(f"==== {cidade.nome} - BANCADAS ====")
            for i, b in enumerate(bancadas, start=1):
                print(f"{i} - {b.tipo}")
            print(f"{len(bancadas) + 1} - Voltar")

            escolha = self._ler_opcao(1, len(bancadas) + 1)
            if escolha == len(bancadas) + 1:
                return

            self._usar_bancada(bancadas[escolha - 1])

    def _visitar_cidade(self, cidade) -> None:
        while True:
            self._clear()
            print(f"==== {cidade.nome} ({cidade.regiao}) ====")
            if cidade.descricao:
                print(cidade.descricao)

            print("\n1 - Bancadas (crafting)")
            print("2 - Banco")
            print("3 - Voltar")

            escolha = self._ler_opcao(1, 3)
            if escolha == 1:
                self._mostrar_bancadas(cidade)
            elif escolha == 2:
                Bank(self.player, self.player_id).abrir()
            else:
                return

    def abrir(self: "CityMenu") -> None:
        while True:
            self._clear()
            print("==== CIDADES ====")
            for i, c in enumerate(self.cidades, start=1):
                print(f"{i} - {c.nome} ({c.regiao})")
            print(f"{len(self.cidades) + 1} - Voltar")

            escolha = self._ler_opcao(1, len(self.cidades) + 1)
            if escolha == len(self.cidades) + 1:
                return

            self._visitar_cidade(self.cidades[escolha - 1])