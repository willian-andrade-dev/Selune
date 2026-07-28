import os
from Database.bank_repository import depositar, sacar


class Bank:
    def __init__(self, player, player_id: int):
        self.player = player
        self.player_id = player_id

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

    def _ler_valor(self, maximo: int) -> int:
        while True:
            entrada = input(f"Quanto? (máximo {maximo}): ").strip()
            try:
                valor = int(entrada)
                if 0 < valor <= maximo:
                    return valor
                print(f"Digite um valor entre 1 e {maximo}.")
            except ValueError:
                print("Digite apenas números.")

    def _confirmar(self, mensagem: str) -> bool:
        return input(f"{mensagem} (s/n): ").strip().lower() == "s"

    def _depositar(self) -> None:
        if self.player.gold <= 0:
            print("Você não tem gold em mãos pra depositar.")
            input("\nPressione Enter para continuar...")
            return

        valor = self._ler_valor(self.player.gold)
        if not self._confirmar(f"Depositar {valor} gold?"):
            print("Operação cancelada.")
            input("\nPressione Enter para continuar...")
            return

        depositar(self.player_id, valor)
        self.player.gold -= valor
        self.player.gold_banco += valor
        print(f"Depositado! Saldo no banco: {self.player.gold_banco}")
        input("\nPressione Enter para continuar...")

    def _sacar(self) -> None:
        if self.player.gold_banco <= 0:
            print("Você não tem gold guardado no banco.")
            input("\nPressione Enter para continuar...")
            return

        valor = self._ler_valor(self.player.gold_banco)
        if not self._confirmar(f"Sacar {valor} gold?"):
            print("Operação cancelada.")
            input("\nPressione Enter para continuar...")
            return

        sacar(self.player_id, valor)
        self.player.gold_banco -= valor
        self.player.gold += valor
        print(f"Sacado! Gold em mãos: {self.player.gold}")
        input("\nPressione Enter para continuar...")

    def abrir(self: "Bank") -> None:
        while True:
            self._clear()
            print("==== BANCO ====")
            print(f"Gold em mãos: {self.player.gold}")
            print(f"Gold guardado no banco: {self.player.gold_banco}")
            print("\n1 - Depositar")
            print("2 - Sacar")
            print("3 - Voltar")

            escolha = self._ler_opcao(1, 3)
            if escolha == 1:
                self._depositar()
            elif escolha == 2:
                self._sacar()
            else:
                return