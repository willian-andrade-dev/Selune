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
    TEXTOS_ABERTURA = {
        'Coleta': "Você encontrou uma planta/material pelo caminho.",
        'Veio de Minério': "Você encontra um veio de minério exposto na rocha.",
        'Cristais Raros': "Cristais brilhantes se destacam entre as pedras.",
        'Cristais de Gelo': "Formações de gelo cristalizado brilham à sua frente.",
        'Cristais de Magma': "Cristais formados pelo calor extremo do vulcão pulsam com um brilho avermelhado.",
        'Veio de Gemas': "Você avista pedras preciosas incrustadas na rocha.",
        'Madeira/Resina de Árvore Gigante': "Uma árvore gigantesca ergue-se diante de você, com resina escorrendo pelo tronco.",
    }

    FAMILIA_POR_EVENTO = {
        'Veio de Minério': 'Mineral',
        'Cristais Raros': 'Cristal',
        'Cristais de Gelo': 'Cristal',
        'Cristais de Magma': 'Cristal',
        'Veio de Gemas': 'Cristal',
        'Madeira/Resina de Árvore Gigante': 'Madeira',
    }

    def __init__(self, player, nome_evento, monstros_disponiveis, localizacao, habilidades, ler_opcao):
        self.player = player
        self.nome_evento = nome_evento
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
        print(self.TEXTOS_ABERTURA.get(self.nome_evento, self.TEXTOS_ABERTURA['Coleta']))
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

class EventoAchado:
    ARMADILHA_CHANCE = 0.12
    ARMADILHA_DANO_PERCENT = 0.15
    CHANCE_ITEM_BONUS = 0.35
    OURO_MIN_POR_DIFICULDADE = 8
    OURO_MAX_POR_DIFICULDADE = 20

    TEXTOS_ABERTURA = {
        'Baú': "Há um baú parcialmente enterrado.",
        'Saco Abandonado': "Há uma mochila esquecida no chão.",
        'Câmara do Tesouro': "Você encontra uma câmara escondida, repleta de riquezas.",
        'Estátua': "Uma antiga estátua observa você. Há algo gravado em sua base.",
        'Sala Secreta': "Você encontrou uma sala secreta escondida, com um baú ao centro. Deseja abrir?"
    }

    REWARD_MULTIPLIER = {
        'Baú': 1.0,
        'Saco Abandonado': 0.6,
        'Câmara do Tesouro': 2.5,
        'Estátua': 1.0,
        'Sala Secreta': 1.0,
    }

    def __init__(self, player, nome_evento, localizacao, ler_opcao):
        self.player = player
        self.nome_evento = nome_evento
        self.localizacao = localizacao
        self.ler_opcao = ler_opcao

    def _faixa_raridade(self) -> str:
        dificuldade = self.localizacao.dificuldade
        if dificuldade <= 2: return 'Comum'
        if dificuldade <= 4: return 'Incomum'
        if dificuldade <= 6: return 'Raro'
        if dificuldade <= 8: return 'Épico'
        return 'Lendário'

    def iniciar(self) -> None:
        print(self.TEXTOS_ABERTURA.get(self.nome_evento, "Você encontra algo interessante."))
        print("1 - Abrir/Examinar")
        print("2 - Ignorar")
        if self.ler_opcao(1, 2) == 2:
            return

        if random.random() < self.ARMADILHA_CHANCE:
            dano = int(self.player.hp_maximo * self.ARMADILHA_DANO_PERCENT)
            self.player.hp = max(self.player.hp - dano, 1)
            print(f"Era uma armadilha! Você perdeu {dano} de HP.")
            return

        multiplicador = self.REWARD_MULTIPLIER.get(self.nome_evento, 1.0)
        dificuldade = self.localizacao.dificuldade

        if self.nome_evento == 'Estátua':
            xp = int(dificuldade * 15 * multiplicador)
            self.player.xp += xp
            self.player.subir_nivel()
            print(f"Você examina a estátua e sente um fluxo de conhecimento antigo. +{xp} XP.")
        else:
            ouro = int(random.randint(
                dificuldade * self.OURO_MIN_POR_DIFICULDADE,
                dificuldade * self.OURO_MAX_POR_DIFICULDADE,
            ) * multiplicador)
            self.player.gold += ouro
            print(f"Você encontrou {ouro} peças de ouro.")

        if random.random() < min(self.CHANCE_ITEM_BONUS * multiplicador, 0.9):
            resultado = sortear_material(self._faixa_raridade())
            if resultado is not None:
                item_id, nome = resultado
                adicionar_item_inventario(self.player.id, item_id, 1)
                print(f"Também encontrou: {nome}.")

class EventoInvestigacao:
    CHANCE_NADA = 0.5
    CHANCE_ITEM = 0.3
    # o restante (0.2) cai em monstro

    TEXTOS_ABERTURA = {
        'Ruínas': "Você encontra uma pequena construção em ruínas.",
        'Eco Misterioso': "Um eco estranho ressoa pelas paredes ao seu redor.",
    }
    TEXTOS_NADA = {
        'Ruínas': "Você explora as ruínas, mas não encontra nada de interessante.",
        'Eco Misterioso': "Você segue o eco, mas ele se dissipa sem deixar rastros.",
    }

    def __init__(self, player, nome_evento, monstros_disponiveis, localizacao, habilidades, ler_opcao):
        self.player = player
        self.nome_evento = nome_evento
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
        print(self.TEXTOS_ABERTURA.get(self.nome_evento, "Você investiga o local."))
        print("1 - Investigar")
        print("2 - Ignorar")
        if self.ler_opcao(1, 2) == 2:
            return

        sorteio = random.random()
        if sorteio < self.CHANCE_NADA:
            print(self.TEXTOS_NADA.get(self.nome_evento, "Nada de interessante aqui."))

        elif sorteio < self.CHANCE_NADA + self.CHANCE_ITEM:
            resultado = sortear_material(self._faixa_raridade())
            if resultado is None:
                print("Você não encontrou nada de útil.")
            else:
                item_id, nome = resultado
                adicionar_item_inventario(self.player.id, item_id, 1)
                print(f"Entre os escombros, você encontra: {nome}.")

        else:
            candidatos = monstros_da_localizacao(self.monstros_disponiveis, self.localizacao)
            if not candidatos:
                print("Você ouve um barulho, mas nada aparece.")
                return
            print("Algo se move nas sombras...")
            monstro = random.choice(candidatos)
            EventoCombateDireto(self.player, monstro, self.localizacao, self.habilidades).iniciar()

SEGUIR_PEGADAS_SUCESSO_CHANCE = 0.7
NOMES_ACHADO_PEGADAS = ['Baú', 'Saco Abandonado', 'Estátua', 'Câmara do Tesouro']


class EventoPegadas:
    def __init__(self, player, monstros_disponiveis, localizacao, habilidades, ler_opcao):
        self.player = player
        self.monstros_disponiveis = monstros_disponiveis
        self.localizacao = localizacao
        self.habilidades = habilidades
        self.ler_opcao = ler_opcao

    def iniciar(self) -> None:
        print("Você encontra pegadas recentes no chão.")
        print("1 - Seguir")
        print("2 - Ignorar")
        if self.ler_opcao(1, 2) == 2:
            return

        if random.random() < SEGUIR_PEGADAS_SUCESSO_CHANCE:
            print("As pegadas te levam a algo interessante...")
            nome_sorteado = random.choice(NOMES_ACHADO_PEGADAS)
            EventoAchado(self.player, nome_sorteado, self.localizacao, self.ler_opcao).iniciar()
        else:
            if random.random() < 0.5:
                print("As pegadas te levam direto a um acampamento inimigo!")
                EventoAcampamento(
                    self.player, self.monstros_disponiveis, self.localizacao,
                    self.habilidades, self.ler_opcao
                ).iniciar()
            else:
                print("Você percebe tarde demais: caiu numa emboscada!")
                grupo = sortear_grupo(self.monstros_disponiveis, NOMES_MONSTROS_EMBOSCADA, self.localizacao)
                GroupCombat(self.player, grupo, self.localizacao, self.habilidades).start()

class EventoRisco:
    DESVIAR_CHANCE = 0.4
    DANO_PERCENT = 0.15

    TEXTOS = {
        'Armadilha': "Você pisa em algo. Clique...",
        'Lava Ativa': "O chão racha e um jorro de lava irrompe perto de você!",
        'Gêiser de Magma': "Um gêiser de magma explode repentinamente ao seu lado!",
        'Rocha Vulcânica': "Uma rocha incandescente se solta e cai em sua direção!",
    }

    def __init__(self, player, nome_evento, localizacao):
        self.player = player
        self.nome_evento = nome_evento
        self.localizacao = localizacao

    def iniciar(self) -> None:
        print(self.TEXTOS.get(self.nome_evento, "Um perigo repentino te pega desprevenido!"))

        if random.random() < self.DESVIAR_CHANCE:
            print("Você percebe a tempo e consegue desviar!")
            return

        dano = int(self.player.hp_maximo * self.DANO_PERCENT)
        self.player.hp = max(self.player.hp - dano, 1)
        print(f"Você não conseguiu escapar! Perdeu {dano} de HP.")

class EventoPortal:
    CHANCE_POSITIVO = 0.5
    QTD_BAUS_POSITIVO = 5
    QTD_MOBS_NEGATIVO = 3

    def __init__(self, player, monstros_disponiveis, localizacoes, localizacao_atual, habilidades, ler_opcao):
        self.player = player
        self.monstros_disponiveis = monstros_disponiveis
        self.localizacoes = localizacoes
        self.localizacao_atual = localizacao_atual
        self.habilidades = habilidades
        self.ler_opcao = ler_opcao

    def _faixa_raridade(self, localizacao) -> str:
        dificuldade = localizacao.dificuldade
        if dificuldade <= 2: return 'Comum'
        if dificuldade <= 4: return 'Incomum'
        if dificuldade <= 6: return 'Raro'
        if dificuldade <= 8: return 'Épico'
        return 'Lendário'

    def _sortear_localizacao_destino(self):
        candidatas = [
            loc for loc in self.localizacoes
            if loc.dificuldade > self.localizacao_atual.dificuldade
        ] or [loc for loc in self.localizacoes if loc.id != self.localizacao_atual.id]
        return random.choice(candidatas) if candidatas else None

    def _resultado_positivo(self, localizacao_destino) -> None:
        print(f"O portal te leva a uma tumba antiga, esquecida perto de {localizacao_destino.nome}.")
        print(f"Você encontra {self.QTD_BAUS_POSITIVO} baús pelo caminho!")

        ouro_total = 0
        itens_encontrados = []
        raridade = self._faixa_raridade(localizacao_destino)

        for _ in range(self.QTD_BAUS_POSITIVO):
            ouro_total += random.randint(
                localizacao_destino.dificuldade * 8,
                localizacao_destino.dificuldade * 20,
            )
            if random.random() < 0.5:
                resultado = sortear_material(raridade)
                if resultado is not None:
                    item_id, nome = resultado
                    adicionar_item_inventario(self.player.id, item_id, 1)
                    itens_encontrados.append(nome)

        self.player.gold += ouro_total
        if itens_encontrados:
            print(f"Você ganhou {ouro_total} de ouro e encontrou: {', '.join(itens_encontrados)}.")
        else:
            print(f"Você ganhou {ouro_total} de ouro.")

    def _resultado_negativo(self, localizacao_destino) -> None:
        print(f"O portal te joga direto numa emboscada perto de {localizacao_destino.nome}!")
        candidatos = monstros_da_localizacao(self.monstros_disponiveis, localizacao_destino)
        if not candidatos:
            print("Você sente uma presença hostil, mas nada aparece. O portal se fecha.")
            return
        grupo = random.choices(candidatos, k=self.QTD_MOBS_NEGATIVO)
        GroupCombat(self.player, grupo, localizacao_destino, self.habilidades).start()

    def iniciar(self) -> None:
        print("Um portal misterioso se abre à sua frente, pulsando com energia desconhecida.")
        print("1 - Atravessar")
        print("2 - Ignorar")
        if self.ler_opcao(1, 2) == 2:
            return

        localizacao_destino = self._sortear_localizacao_destino()
        if localizacao_destino is None:
            print("O portal se fecha sem levar você a lugar nenhum.")
            return

        if random.random() < self.CHANCE_POSITIVO:
            self._resultado_positivo(localizacao_destino)
        else:
            self._resultado_negativo(localizacao_destino)

class EventoCura:
    MALDICAO_DURACAO_TURNOS = 3
    BUFF_DURACAO_TURNOS = 3

    def __init__(self, player, nome_evento, monstros_disponivels, localizacao, habilidade, ler_opcao):
        self.player = player
        self.nome_evento = nome_evento
        self.monstros_disponiveis = monstros_disponiveis
        self.localizacao = localizacao
        self.habilidades = habilidades
        self.ler_opcao = ler_opcao

    def iniciar(self) -> None:
        if self.nome_evento == 'Santuário':
            self._santuario()
        elif self.nome_evento == 'Fonte Mágica':
            self._fonte_magica()
        else:
            self._altar_antigo()

    # ---------- Santuário: sempre bom, sem risco ----------
    def _santuario(self) -> None:
        print("Você encontra um santuário sereno, envolto em luz suave.")
        print("1 - Descansar")
        print("2 - Ignorar")
        if self.ler_opcao(1, 2) == 2:
            return

        self.player.hp = self.player.hp_maximo
        self.player.mana = self.player.mana_maximo
        self.player.buffs_ativos = [b for b in self.player.buffs_ativos if b["valor"] > 0]
        self.player.atualizar_status()
        print("Você sente uma paz absoluta. HP e mana totalmente restaurados, e suas aflições foram removidas.")

    # ---------- Fonte Mágica: beber é uma loteria (com chance de maldição) ----------
    def _fonte_magica(self) -> None:
        print("Águas cristalinas emanam energia mágica.")
        print("1 - Beber")
        print("2 - Ignorar")
        if self.ler_opcao(1, 2) == 2:
            return

        sorteio = random.random()
        if sorteio < 0.4:
            self.player.mana = self.player.mana_maximo
            print("A água enche você de energia arcana. Mana totalmente restaurada.")
        elif sorteio < 0.7:
            cura = int(self.player.hp_maximo * 0.3)
            self.player.hp = min(self.player.hp + cura, self.player.hp_maximo)
            print(f"A água cura seus ferimentos. +{cura} HP.")
        elif sorteio < 0.9:
            self.player.aplicar_buff("buff_ataque", 8, self.BUFF_DURACAO_TURNOS)
            print("Você sente sua força aumentar temporariamente!")
        else:
            self.player.aplicar_buff("buff_ataque", -6, self.MALDICAO_DURACAO_TURNOS)
            print("A água estava amaldiçoada! Você sente sua força diminuir.")

    # ---------- Altar Antigo: rezar, destruir ou ignorar ----------
    def _altar_antigo(self) -> None:
        print("Há um altar coberto de musgo diante de você.")
        print("1 - Rezar")
        print("2 - Destruir")
        print("3 - Ignorar")
        escolha = self.ler_opcao(1, 3)

        if escolha == 3:
            return

        if escolha == 1:
            sorteio = random.random()
            if sorteio < 0.4:
                cura = int(self.player.hp_maximo * 0.25)
                self.player.hp = min(self.player.hp + cura, self.player.hp_maximo)
                print(f"Você reza diante do altar e sente suas feridas se fecharem. +{cura} HP.")
            elif sorteio < 0.7:
                mana = int(self.player.mana_maximo * 0.25)
                self.player.mana = min(self.player.mana + mana, self.player.mana_maximo)
                print(f"Você reza diante do altar e sente sua mana se renovar. +{mana} de mana.")
            else:
                self.player.aplicar_buff("buff_armadura", 6, self.BUFF_DURACAO_TURNOS)
                print("Uma proteção sutil envolve seu corpo.")
        else:
            print("Ao destruir o altar, um espírito vingativo se manifesta!")
            candidatos = monstros_da_localizacao(self.monstros_disponiveis, self.localizacao)
            if not candidatos:
                print("Uma presença hostil paira no ar, mas nada se materializa.")
                return
            monstro = random.choice(candidatos)
            GroupCombat(self.player, [monstro], self.localizacao, self.habilidades).start()