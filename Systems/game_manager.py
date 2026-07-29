from Entities.player import Player
from Systems.combat import Combat
from Systems.shop import Shop
from Database.player_repository import buscar_player, salvar_player
from Database.item_repository import carregar_itens
from Database.monster_repository import carregar_monstros
from Database.location_repository import carregar_localizacoes
from Database.inventory_repository import carregar_inventario_jogador
from Database.class_repository import carregar_classes, carregar_habilidades
from World.location import Localização
from Systems.exploration import Exploration
from Systems.character_creation import CharacterCreation
from Database.equipment_repository import desequipar_item
from Systems.city import CityMenu
from Database.city_repository import carregar_cidades
from Database.recipe_repository import carregar_receitas
from Systems.exploration_events import (
    sortear_evento,
    EventoCombateDireto,
    EventoAcampamento,
    EventoDescanso,
    EventoColeta,
    EventoAchado,
    EventoInvestigacao,
    EventoPegadas,
    EventoRisco,
    EventoPortal,
    EventoCura
)
import os

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Entities.classes import Classe


class Game:
    def __init__(self: 'Game') -> None:
        self.itens = carregar_itens()
        self.monstros = carregar_monstros(self.itens)
        self.localizacoes = carregar_localizacoes()
        self.classes = carregar_classes()
        self.habilidades = carregar_habilidades()
        self.cidades = carregar_cidades()
        self.exploration = Exploration(self.localizacoes, self.monstros)
        self.character_creation = CharacterCreation(self.itens)
        self.receitas_por_item = carregar_receitas(self.itens)

    def limpar_tela(self: 'Game') -> None:
        os.system('cls' if os.name == 'nt' else 'clear')

    def selecionar_classe(self: 'Game') -> 'Classe':
        print("\n=== ESCOLHA SUA CLASSE ===")
        for i, c in enumerate(self.classes, start=1):
            print(f"{i} - {c.nome}: {c.descricao}")
        escolha = self.ler_opcao("Escolha uma classe: ", 1, len(self.classes))
        return self.classes[escolha - 1]

    def menu_personagem(self, player, player_id):
        while True:
            self.limpar_tela()
            print("1 - Status")
            print("2 - Equipamentos")
            print("3 - Voltar")
            escolha = self.ler_opcao("Escolha uma opção: ", 1, 3)

            if escolha == 1:
                player.mostrar_status()
                input("\nPressione Enter para continuar...")

            elif escolha == 2:
                self.menu_equipamentos(player, player_id)

            else:
                break

    def menu_equipamentos(self, player, player_id):
        while True:
            self.limpar_tela()
            player.equipamento.mostrar_equipamento()
            print("\n1 - Desequipar item")
            print("2 - Ver equipamentos no inventário")
            print("3 - Voltar")
            escolha = self.ler_opcao("Escolha uma opção: ", 1, 3)

            if escolha == 1:
                self._desequipar_item(player, player_id)

            elif escolha == 2:
                self._mostrar_equipaveis_inventario(player, player_id)

            else:
                break

    def _mostrar_equipaveis_inventario(self, player, player_id):
        equipaveis = player.inventario.listar_equipaveis()

        if not equipaveis:
            print("Você não tem armas, armaduras ou acessórios no inventário.")
            input("\nPressione Enter para voltar...")
            return

        print("\n=== ARMAS, ARMADURAS E ACESSÓRIOS ===")
        for i, (item, quantidade) in enumerate(equipaveis, start=1):
            print(f"{i} - {item} x{quantidade}")
        print(f"{len(equipaveis) + 1} - Voltar")

        escolha = self.ler_opcao("Escolha um item para equipar: ", 1, len(equipaveis) + 1)
        if escolha == len(equipaveis) + 1:
            return

        item_escolhido, _ = equipaveis[escolha - 1]
        equipou = item_escolhido.use(player)
        if equipou:
            salvar_player(player, player_id)
        input("\nPressione Enter para continuar...")

    def _desequipar_item(self, player, player_id):
        print("\n1 - Arma")
        print("2 - Armadura")
        print("3 - Anel")
        print("4 - Colar")
        print("5 - Amuleto")
        print("6 - Brinco")
        print("7 - Cancelar")
        escolha = self.ler_opcao("O que deseja desequipar? ", 1, 7)

        if escolha == 1:
            player.equipamento.desequipar_arma()
            desequipar_item(player_id, "arma")
        elif escolha == 2:
            player.equipamento.desequipar_armadura()
            desequipar_item(player_id, "armadura")
        elif escolha in (3, 4, 5, 6):
            slots = {3: "Anel", 4: "Colar", 5: "Amuleto", 6: "Brinco"}
            slot = slots[escolha]
            player.equipamento.desequipar_acessorio(slot)
            desequipar_item(player_id, slot)
        else:
            return

        player.atualizar_status()
        salvar_player(player, player_id)
        input("\nPressione Enter para continuar...")

    def menu_inventario(self, player, player_id):
        while True:
            if not player.inventario.itens:
                print("Seu inventário está vazio.")
                input("\nPressione Enter para voltar...")
                return

            player.inventario.mostrar_inventario()
            print("\n1 - Usar/Equipar um item")
            print("2 - Voltar")
            escolha = self.ler_opcao("Escolha uma opção: ", 1, 2)

            if escolha == 1:
                nome_item = input("Nome do item: ")
                item = player.inventario.procurar_item(nome_item)
                if item is None:
                    print("Item não encontrado.")
                else:
                    item.use(player)
                    salvar_player(player, player_id)
                input("\nPressione Enter para continuar...")
            else:
                break

    def selecionar_localizacao(self: 'Game') -> 'Localização':
        localizacoes_ordenadas = self.exploration.localizacoes_ordenadas()

        print("\n=== LOCALIZAÇÕES ===")
        for i, loc in enumerate(localizacoes_ordenadas, start=1):
            print(f"{i} - {loc.nome} (Nível {loc.dificuldade})")
        print(f"{len(localizacoes_ordenadas) + 1} - Voltar")

        escolha = self.ler_opcao("Escolha uma localização: ", 1, len(localizacoes_ordenadas) + 1)
        if escolha == len(localizacoes_ordenadas) + 1:
            return None
        return localizacoes_ordenadas[escolha - 1]

    def menu_explorar(self: 'Game', player: 'Player', player_id: int) -> None:
        while True:
            self.limpar_tela()
            print("1 - Localizações")
            print("2 - Usar poção")
            print("3 - Voltar")
            escolha = self.ler_opcao("Escolha uma opção: ", 1, 3)

            if escolha == 1:
                localizacao = self.selecionar_localizacao()
                if localizacao is None:
                    continue

                self._processar_evento(player, localizacao)
                salvar_player(player, player_id)
                input("\nPressione Enter para continuar...")

            elif escolha == 2:
                player.usar_pocao(lambda mi, ma: self.ler_opcao("Escolha uma opção: ", mi, ma))
                salvar_player(player, player_id)
                input("\nPressione Enter para continuar...")

            else:
                break

    def _processar_evento(self, player, localizacao) -> None:
        evento = sortear_evento(localizacao)
        if evento is None:
            print(f"Nada de interessante em {localizacao.nome} por enquanto.")
            return

        _, nome_evento, tipo_evento, _ = evento
        ler_opcao_wrapper = lambda mi, ma: self.ler_opcao("Escolha uma opção: ", mi, ma)

        if tipo_evento == 'combate_direto':
            monstro_escolhido = self.exploration.sortear_monstro(localizacao)
            if monstro_escolhido is None:
                print(f"Nenhum monstro encontrado em {localizacao.nome}.")
                return
            EventoCombateDireto(player, monstro_escolhido, localizacao, self.habilidades).iniciar()

        elif tipo_evento == 'acampamento':
            EventoAcampamento(player, self.monstros, localizacao, self.habilidades, ler_opcao_wrapper).iniciar()

        elif tipo_evento == 'descanso':
            EventoDescanso(player, self.monstros, localizacao, self.habilidades, ler_opcao_wrapper).iniciar()

        elif tipo_evento == 'coleta':
            EventoColeta(player, nome_evento, self.monstros, localizacao, self.habilidades, ler_opcao_wrapper).iniciar()

        elif tipo_evento == 'achado':
            EventoAchado(player, nome_evento, localizacao, ler_opcao_wrapper).iniciar()

        elif tipo_evento == 'pegadas':
            EventoPegadas(player, self.monstros, localizacao, self.habilidades, ler_opcao_wrapper).iniciar()

        elif tipo_evento == 'investigacao':
            EventoInvestigacao(player, nome_evento, self.monstros, localizacao, self.habilidades, ler_opcao_wrapper).iniciar()

        elif tipo_evento == 'risco':
            EventoRisco(player, nome_evento, localizacao).iniciar()

        elif tipo_evento == 'portal':
            EventoPortal(player, self.monstros, self.localizacoes, localizacao, self.habilidades, ler_opcao_wrapper).iniciar()

        elif tipo_evento == 'cura':
            EventoCura(player, nome_evento, self.monstros, localizacao, self.habilidades, ler_opcao_wrapper).iniciar()

        else:
            print(f"Evento desconhecido: {nome_evento}")

    def ler_opcao(self: 'Game', mensagem: str, minimo: int, maximo: int) -> int:
        while True:
            try:
                valor = int(input(mensagem))
                if minimo <= valor <= maximo:
                    return valor
                print(f"Digite um número entre {minimo} e {maximo}.")
            except ValueError:
                print("Digite apenas números.")

    def run(self: 'Game') -> None:
        rpg_program = True
        while rpg_program:
            print("1 - Criar personagem novo")
            print("2 - Carregar personagem existente")
            print("3 - Log Out")
            opcao_inicial = self.ler_opcao("Escolha: ", 1, 3)

            if opcao_inicial == 1:
                nome = input("Nome do personagem: ")
                classe_escolhida = self.selecionar_classe()
                player, player_id = self.character_creation.criar_personagem(nome, classe_escolhida)
                print(f"Personagem {nome} ({classe_escolhida.nome}) criado com ID {player_id}!")

            elif opcao_inicial == 2:
                player_id = self.ler_opcao("Digite o ID do seu personagem: ", 1, 999999)
                player = buscar_player(player_id, self.itens)   
                if player is None:
                    print("Personagem não encontrado.")
                    continue
                player.inventario.itens = carregar_inventario_jogador(player_id, self.itens)
                print(f"Bem-vindo de volta, {player.nome}!")

            elif opcao_inicial == 3:
                print("See you later")
                rpg_program = False
                continue

            else:
                print("Opção inválida.")
                continue

            jogando = True
            while jogando:
                self.limpar_tela()
                print("1 - Personagem")
                print("2 - Explorar")
                print("3 - Inventário")
                print("4 - Loja")
                print("5 - Cidades")
                print("6 - Log Out")
                option = self.ler_opcao("Escolha uma opção: ", 1, 6)

                if option == 1:
                    self.menu_personagem(player, player_id)
                elif option == 2:
                    self.menu_explorar(player, player_id)
                elif option == 3:
                    self.menu_inventario(player, player_id)
                elif option == 4:
                    Shop(player, player_id).abrir()
                    salvar_player(player, player_id)
                elif option == 5:
                    CityMenu(self.cidades, player, player_id, self.receitas_por_item).abrir()
                    salvar_player(player, player_id)
                elif option == 6:
                    print(f"See you later, {player.nome}")
                    jogando = False
                else:
                    print("Opção inválida.")