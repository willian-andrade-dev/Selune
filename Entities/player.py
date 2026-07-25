from typing import TYPE_CHECKING
from Entities.inventory import Inventory
from Entities.equipment import Equipment
from Entities.classes import Classe

if TYPE_CHECKING:
    from Entities.monster import Monstro

class Player:
    def __init__(self: 'Player', nome: str, hp: int, mana: int, gold: int, xp: int, level: int,
                 ataque: int, armadura: int, classe_id: int) -> None:
        self.id = None
        self.nome = nome
        self.hp_maximo = hp
        self.hp = hp
        self.mana = mana
        self.gold = gold
        self.xp = xp
        self.xp_para_upar = 75
        self.level = level
        self.ataque_base = ataque
        self.ataque = ataque
        self.armadura_base = armadura
        self.armadura = armadura
        self.classe_id = classe_id
        self.buffs_ativos = []
        self.inventario = Inventory()
        self.equipamento = Equipment()

    def __str__(self):
        return f"{self.nome} | Level {self.level} | HP: {self.hp}/{self.hp_maximo} | XP: {self.xp}"

    def atacar(self: 'Player', monstro: 'Monstro') -> None:
        print(f"HP: {monstro.hp}, Ataque: {monstro.ataque}")
        monstro.hp = monstro.hp - self.ataque
        print(f"{monstro.nome} HP: {monstro.hp}")

    def mostrar_status(self: 'Player') -> None:
        print(f"Nome: {self.nome}") 
        print(f"HP Atual: {self.hp}") 
        print(f"HP Máximo {self.hp_maximo}")
        print(f"Mana: {self.mana}") 
        print(f"Gold: {self.gold}")
        print(f"Armadura: {self.armadura}")
        print(f"Ataque base: {self.ataque_base}")
        print(f"Ataque: {self.ataque}")
        print(f"XP: {self.xp}") 
        print(f"Level: {self.level}")


    def usar_pocao_cura(self: 'Player', ler_opcao) -> bool:
        """ler_opcao: função(minimo, maximo) -> int. Retorna True se uma poção foi usada."""
        pocoes = self.inventario.listar_pocoes_cura()

        if not pocoes:
            print("Você não tem nenhuma poção de cura no inventário!")
            return False

        print("\n=== POÇÕES DISPONÍVEIS ===")
        for i, (item, quantidade) in enumerate(pocoes, start=1):
            print(f"{i} - {item.nome} ({item.descricao_cura()}) x{quantidade}")
        print(f"{len(pocoes) + 1} - Cancelar")

        escolha = ler_opcao(1, len(pocoes) + 1)
        if escolha == len(pocoes) + 1:
            return False

        item_escolhido, _ = pocoes[escolha - 1]
        item_escolhido.use(self)
        return True

    def habilidades_disponiveis(self: 'Player', todas_habilidades: list) -> list:
        return [h for h in todas_habilidades
                if h.classe_id == self.classe_id and h.nivel_requerido <= self.level]

    def aplicar_buff(self: 'Player', tipo: str, valor: int, duracao_turnos: int) -> None:
        self.buffs_ativos.append({"tipo": tipo, "valor": valor, "turnos_restantes": duracao_turnos})
        self.atualizar_status()

    def atualizar_buffs_turno(self: 'Player') -> None:
        if not self.buffs_ativos:
            return
        for buff in self.buffs_ativos:
            buff["turnos_restantes"] -= 1
        self.buffs_ativos = [b for b in self.buffs_ativos if b["turnos_restantes"] > 0]
        self.atualizar_status()

    def atualizar_status(self: 'Player') -> None:
        self.ataque = self.ataque_base
        if self.equipamento.arma is not None:
            self.ataque += self.equipamento.arma.dano

        self.armadura = self.armadura_base
        if self.equipamento.armadura is not None:
            self.armadura += self.equipamento.armadura.armadura

        for buff in self.buffs_ativos:
            if buff["tipo"] == "buff_ataque":
                self.ataque += buff["valor"]
            elif buff["tipo"] == "buff_armadura":
                self.armadura += buff["valor"]

    def subir_nivel(self: 'Player') -> None:
        while self.xp >= self.xp_para_upar:
            self.xp -= self.xp_para_upar
            self.level += 1
            self.ataque_base += 2 # valor que aumenta por nivel
            self.hp_maximo += 5 # valor que aumenta por nivel
            print(f"{self.nome} subiu para o nível {self.level}!")
        self.atualizar_status()