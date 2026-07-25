from typing import TYPE_CHECKING
from Entities.inventory import Inventory
from Entities.equipment import Equipment
from Entities.classes import Classe
from datetime import datetime, timedelta

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
        self.level = level
        self.xp_para_upar = self._calcular_xp_para_upar()
        self.ataque_base = ataque
        self.ataque = ataque
        self.armadura_base = armadura
        self.armadura = armadura
        self.classe_id = classe_id
        self.energia_maxima = 30
        self.energia_atual = 30
        self.cansado_desde = None
        self.buffs_ativos = []
        self.inventario = Inventory()
        self.equipamento = Equipment()

    def __str__(self):
        return f"{self.nome} | Level {self.level} | HP: {self.hp}/{self.hp_maximo} | XP: {self.xp}"

    def _calcular_xp_para_upar(self: 'Player') -> int:
        """XP necessário para sair do nível atual e ir para o próximo.
        Curva exponencial: rápida até ~nível 50-60 (progressão principal),
        dispara nos níveis finais (60-100) — o nível 100 fica reservado
        pra quem realmente dedicar um grind longo."""
        BASE_XP = 15
        GROWTH = 1.128
        return int(BASE_XP * (GROWTH ** (self.level - 1)))

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


    def usar_pocao(self: 'Player', ler_opcao) -> bool:
        """ler_opcao: função(minimo, maximo) -> int. Retorna True se uma poção foi usada."""
        pocoes = self.inventario.listar_pocoes()

        if not pocoes:
            print("Você não tem nenhuma poção no inventário!")
            return False

        print("\n=== POÇÕES DISPONÍVEIS ===")
        for i, (item, quantidade) in enumerate(pocoes, start=1):
            print(f"{i} - {item.nome} ({item.descricao_efeito()}) x{quantidade}")
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
            self.xp_para_upar = self._calcular_xp_para_upar()
            print(f"{self.nome} subiu para o nível {self.level}!")
        self.atualizar_status()

    def pode_lutar(self) -> tuple[bool, str]:
        if self.energia_atual > 0:
            return True, ""

        if self.cansado_desde is None:
            self.cansado_desde = datetime.now()
            return False, "Você está exausto! Descanse por 1 hora."

        tempo_passado = datetime.now() - self.cansado_desde
        if tempo_passado >= timedelta(hours=1):
            self.energia_atual = self.energia_maxima
            self.cansado_desde = None
            return True, ""

        restante = timedelta(hours=1) - tempo_passado
        minutos = int(restante.total_seconds() // 60)
        return False, f"Ainda cansado. Faltam {minutos} minutos de descanso."

    def consumir_energia(self) -> None:
        self.energia_atual -= 1
        if self.energia_atual == 0:
            self.cansado_desde = datetime.now()