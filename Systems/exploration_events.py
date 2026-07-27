import random

from Systems.combat import Combat
from Systems.group_combat import GroupCombat
from Systems.monster_utils import monstros_da_localizacao, sortear_grupo
from Database.event_repository import carregar_eventos_localizacao, sortear_material
from Database.inventory_repository import adicionar_item_inventario


ESPIONAGEM_CHANCE = 0.6
DESCANSO_HP_PERCENT = 0.2
DESCANSO_MANA_PERCENT = 0.2
DESCANSO_EMBOSCADA_CHANCE = 0.15 
COLETA_SUCESSO_CHANCE = 0.8

NOMES_MONSTROS_ACAMPAMENTO = [
    "Bandido Novato", "Bandido Florestal", "Orc Guerreiro", "Gnoll Caçador",
    "Esqueleto Guerreiro", "Zumbi", "Ladrão do Deserto",
]

NOMES_MONSTROS_EMBOSCADA = [
    "Javali Selvagem", "Lobo Filhote", "Bandido Novato", "Bandido Florestal",
    "Orc Guerreiro", "Gnoll Caçador", "Esqueleto Guerreiro", "Zumbi",
    "Ladrão do Deserto", "Lobo Sombrio", "Lobo Glacial",
]

def sortear_evento(localizacao) -> tuple[int, str, str, int] | None:
    """Sorteia um evento ponderado pelos pesos da localização."""
    eventos = carregar_eventos_localizacao(localizacao.id)
    if not eventos:
        return None
    pesos = [peso for (_, _, _, peso) in eventos]
    return random.choices(eventos, weights=pesos)[0]


class EventoCombateDireto:
    def __init__(self, player, monstro, localizacao, habilidades):
        self.player = player
        self.monstro = monstro
        self.localizacao = localizacao
        self.habilidades = habilidades

    def iniciar(self) -> None:
        print(f"Você escuta passos... um {self.monstro.nome} aparece!")
        Combat(self.player, self.monstro, self.localizacao, self.habilidades).start()


class EventoAcampamento:
    def __init__(self, player, monstros_disponiveis, localizacao, habilidades, ler_opcao):
        self.player = player
        self.localizacao = localizacao
        self.grupo = sortear_grupo(monstros_disponiveis, NOMES_MONSTROS_ACAMPAMENTO, localizacao)
        self.habilidades = habilidades
        self.ler_opcao = ler_opcao

    def iniciar(self) -> None:
        print("Você avista fumaça entre as árvores. Há um pequeno acampamento inimigo.")
        print("Eles ainda não perceberam sua presença.")
        print("1 - Atacar")
        print("2 - Espionar")
        print("3 - Fugir")
        escolha = self.ler_opcao(1, 3)

        if escolha == 3:
            print("Você se afasta silenciosamente.")
            return

        if escolha == 2:
            if random.random() < ESPIONAGEM_CHANCE:
                nomes = ", ".join(m.nome for m in self.grupo)
                print(f"Você observa de longe... o grupo é: {nomes}.")
                print("1 - Atacar agora")
                print("2 - Ir embora")
                if self.ler_opcao(1, 2) == 2:
                    print("Você decide ir embora.")
                    return
            else:
                print("Você faz barulho. Eles perceberam você!")

        GroupCombat(self.player, self.grupo, self.localizacao, self.habilidades).start()


class EventoDescanso:
    def __init__(self, player, monstros_disponiveis, localizacao, habilidades, ler_opcao):
        self.player = player
        self.monstros_disponiveis = monstros_disponiveis
        self.localizacao = localizacao
        self.habilidades = habilidades
        self.ler_opcao = ler_opcao

    def iniciar(self) -> None:
        print("Você encontra uma clareira tranquila, com uma pequena fogueira apagada.")
        print("Parece um bom lugar para descansar.")
        print("1 - Descansar")
        print("2 - Continuar explorando")
        if self.ler_opcao(1, 2) == 2:
            return

        if random.random() < DESCANSO_EMBOSCADA_CHANCE:
            candidatos = monstros_da_localizacao(self.monstros_disponiveis, self.localizacao)
            if not candidatos:
                print("Você ouve algo ao longe, mas nada aparece.")
            else:
                print("Enquanto descansava... um monstro te encontrou!")
                monstro = random.choice(candidatos)
                EventoCombateDireto(self.player, monstro, self.localizacao, self.habilidades).iniciar()
            return

        cura_hp = int(self.player.hp_maximo * DESCANSO_HP_PERCENT)
        cura_mana = int(self.player.mana_maximo * DESCANSO_MANA_PERCENT)
        self.player.hp = min(self.player.hp + cura_hp, self.player.hp_maximo)
        self.player.mana = min(self.player.mana + cura_mana, self.player.mana_maximo)
        print(f"Você descansa e recupera {cura_hp} de HP e {cura_mana} de mana.")


class EventoColeta:
    def __init__(self, player, monstros_disponiveis, localizacao, habilidades, ler_opcao):
        self.player = player
        self.monstros_disponiveis = monstros_disponiveis
        self.localizacao = localizacao
        self.habilidades = habilidades
        self.ler_opcao = ler_opcao

    def _faixa_raridade(self) -> str:
        dificuldade = self.localizacao.dificuldade
        if dificuldade <= 2: return 'Comum'
        if dificuldade <= 4: return 'Incomum'
        if dificuldade <= 6: return 'Raro'
        if dificuldade <= 8: return 'Épico'
        return 'Lendário'

    def iniciar(self) -> None:
        print("Você encontrou uma planta/material pelo caminho.")
        print("1 - Coletar")
        print("2 - Ignorar")
        if self.ler_opcao(1, 2) == 2:
            return

        if random.random() < COLETA_SUCESSO_CHANCE:
            resultado = sortear_material(self._faixa_raridade())
            if resultado is None:
                print("Você não encontrou nada de útil.")
                return
            item_id, nome = resultado
            adicionar_item_inventario(self.player.id, item_id, 1)
            print(f"{nome} obtido.")
        else:
            print("Ao coletar, você faz barulho. Algo ouviu...")
            grupo = sortear_grupo(self.monstros_disponiveis, NOMES_MONSTROS_EMBOSCADA, self.localizacao)
            GroupCombat(self.player, grupo, self.localizacao, self.habilidades).start()