from typing import TYPE_CHECKING
from Entities.inventory import Inventory
from Entities.equipment import Equipment
from Entities.classes import Classe
from datetime import datetime, timedelta
import random

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
        self.critico = 0.0
        self.dano_critico = 50.0       # multiplicador base de dano crítico (50% a mais)
        self.esquiva = 0.0
        self.precisao = 0.0
        self.velocidade = 0.0
        self.roubo_vida = 0.0
        self.mana_por_turno = 0.0
        self.hp_por_turno = 0.0
        self.bonus_xp = 0.0             # %
        self.bonus_ouro = 0.0           # %
        self.resistencias = {
            "fogo": 0.0, "gelo": 0.0, "raio": 0.0,
            "veneno": 0.0, "trevas": 0.0, "luz": 0.0,
        }
        self.classe_id = classe_id
        self.energia_maxima = 30
        self.energia_atual = 30
        self.cansado_desde = None
        self.buffs_ativos = []
        self.inventario = Inventory()
        self.equipamento = Equipment()
        self.cooldowns_habilidades = {}

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
        critico = random.random() < (self.critico / 100)
        dano = self.ataque
        if critico:
            dano = int(dano * (1 + self.dano_critico / 100))

        monstro.hp -= dano
        prefixo = "CRÍTICO! " if critico else ""
        print(f"{prefixo}{self.nome} causou {dano} de dano em {monstro.nome} (HP: {monstro.hp})")

        if self.roubo_vida > 0:
            cura = int(dano * (self.roubo_vida / 100))
            if cura > 0:
                hp_antes = self.hp
                self.hp = min(self.hp + cura, self.hp_maximo)
                curado = self.hp - hp_antes
                if curado > 0:
                    print(f"{self.nome} roubou {curado} de vida! HP: {self.hp}/{self.hp_maximo}")

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

    def _itens_equipados(self) -> list:
        itens = [self.equipamento.arma, self.equipamento.armadura]
        itens += list(self.equipamento.acessorios.values())
        return [i for i in itens if i is not None]

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

            # --- reseta e reagrega os stats secundários a partir dos item_effects ---
        self.critico = 0.0
        self.dano_critico = 50.0
        self.esquiva = 0.0
        self.precisao = 0.0
        self.velocidade = 0.0
        self.roubo_vida = 0.0
        self.mana_por_turno = 0.0
        self.hp_por_turno = 0.0
        self.bonus_xp = 0.0
        self.bonus_ouro = 0.0
        self.resistencias = {k: 0.0 for k in self.resistencias}

        for item in self._itens_equipados():
            for efeito in item.efeitos:
                atributo, valor = efeito["atributo"], efeito["valor"]
                if atributo == "critico":
                    self.critico += valor
                elif atributo == "dano_critico":
                    self.dano_critico += valor
                elif atributo == "esquiva":
                    self.esquiva += valor
                elif atributo == "precisao":
                    self.precisao += valor
                elif atributo == "velocidade":
                    self.velocidade += valor
                elif atributo == "roubo_vida":
                    self.roubo_vida += valor
                elif atributo == "mana_por_turno":
                    self.mana_por_turno += valor
                elif atributo == "hp_por_turno":
                    self.hp_por_turno += valor
                elif atributo == "xp":
                    self.bonus_xp += valor
                elif atributo == "ouro":
                    self.bonus_ouro += valor
                elif atributo.startswith("resistencia_"):
                    elemento = atributo.replace("resistencia_", "")
                    if elemento in self.resistencias:
                        self.resistencias[elemento] += valor
                elif atributo in ("hp_maximo", "mana_maxima", "ataque", "armadura"):
                    pass  # tratados à parte, se algum dia um acessório também bonificar isso direto

    def atualizar_cooldowns_turno(self: 'Player') -> None:
        if not self.cooldowns_habilidades:
            return
        for hid in list(self.cooldowns_habilidades):
            self.cooldowns_habilidades[hid] -= 1
            if self.cooldowns_habilidades[hid] <= 0:
                del self.cooldowns_habilidades[hid]

    def atualizar_regen_turno(self: 'Player') -> None:
        if self.hp_por_turno > 0:
            self.hp = min(self.hp + int(self.hp_por_turno), self.hp_maximo)
        if self.mana_por_turno > 0:
            self.mana += int(self.mana_por_turno)

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