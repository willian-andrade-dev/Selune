from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Entities.item import Weapon, Armadura, Acessorio

class Equipment:
    def __init__(self: 'Equipment') -> None:
        self.arma = None
        self.armadura = None
        self.acessorio = None
    
    def equipar_arma(self: 'Equipment', arma: 'Weapon') -> None:
        self.arma = arma
        print(f"{arma.nome} equipada!")

    def equipar_armadura(self: 'Equipment', armadura: 'Armadura') -> None:
        self.armadura = armadura
        print(f"{armadura.nome} equipada!")

    def equipar_acessorio(self: 'Equipment', acessorio: 'Acessorio') -> None:
        self.acessorio = acessorio
        print(f"{acessorio.nome} equipado!")

    def mostrar_equipamento(self: 'Equipment') -> None:
        print("==== EQUIPAMENTO ====")
        slots = {
            "Arma": self.arma,
            "Armadura": self.armadura,
            "Acessório": self.acessorio,
        }
        for nome_slot, item in slots.items():
            if item is None:
                print(f"{nome_slot}: nenhum")
            else:
                print(f"{nome_slot}: {item.nome}")
            
