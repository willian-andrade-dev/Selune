from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Entities.item import Weapon, Armadura, Acessorio

class Equipment:
    def __init__(self: 'Equipment') -> None:
        self.arma = None
        self.armadura = None
        self.acessorios = {
            "Anel": None,
            "Colar": None,
            "Amuleto": None,
            "Brinco": None,
        }

    def equipar_arma(self: 'Equipment', arma: 'Weapon') -> None:
        self.arma = arma
        print(f"{arma.nome} equipada!")

    def desequipar_arma(self: 'Equipment') -> None:
        if self.arma is None:
            print("Nenhuma arma equipada.")
            return
        print(f"{self.arma.nome} desequipada.")
        self.arma = None

    def equipar_armadura(self: 'Equipment', armadura: 'Armadura') -> None:
        self.armadura = armadura
        print(f"{armadura.nome} equipada!")

    def desequipar_armadura(self: 'Equipment') -> None:
        if self.armadura is None:
            print("Nenhuma armadura equipada.")
            return
        print(f"{self.armadura.nome} desequipada.")
        self.armadura = None

    def equipar_acessorio(self: 'Equipment', acessorio: 'Acessorio') -> None:
        slot = acessorio.subtipo  # 'Anel', 'Colar', 'Amuleto' ou 'Brinco'
        self.acessorios[slot] = acessorio
        print(f"{acessorio.nome} equipado no slot {slot}!")

    def desequipar_acessorio(self: 'Equipment', slot: str) -> None:
        item = self.acessorios.get(slot)
        if item is None:
            print(f"Nenhum acessório equipado no slot {slot}.")
            return
        print(f"{item.nome} desequipado.")
        self.acessorios[slot] = None

    def mostrar_equipamento(self: 'Equipment') -> None:
        print("==== EQUIPAMENTO ====")
        print(f"Arma: {self.arma.nome if self.arma else 'nenhuma'}")
        print(f"Armadura: {self.armadura.nome if self.armadura else 'nenhuma'}")
        for slot, item in self.acessorios.items():
            print(f"{slot}: {item.nome if item else 'nenhum'}")