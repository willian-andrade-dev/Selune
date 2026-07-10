from Entities.player import Player
from Systems.combat import Combat
from Database.player_repository import criar_player, buscar_player, salvar_player
from Database.item_repository import carregar_itens
from Database.monster_repository import carregar_monstros
from Database.location_repository import carregar_localizacoes
from Database.inventory_repository import adicionar_item_inventario
import random
import os
import copy

class Game:
    def __init__(self: 'Game') -> None:
        self.itens = carregar_itens()
        self.monstros = carregar_monstros(self.itens)
        self.localizacoes = carregar_localizacoes()

    def limpar_tela(self: 'Game') -> None:
        os.system('cls' if os.name == 'nt' else 'clear')

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
                player_id = criar_player(nome, 20, 20, 5, 15, 0, 75, 1, 10, 10, 0, 0)
                player = Player(nome, 20, 5, 15, 0, 1, 10, 0)
                player.id = player_id
                print(f"Personagem {nome} criado com ID {player_id}!")

            elif opcao_inicial == 2:
                player_id = self.ler_opcao("Digite o ID do seu personagem: ", 1, 999999)
                player = buscar_player(player_id)
                if player is None:
                    print("Personagem não encontrado.")
                    continue
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
                print("1 - Mostrar status")
                print("2 - Atacar criatura")
                print("3 - Se curar")
                print("4 - Mostrar inventário")
                print("5 - Log Out")
                option = self.ler_opcao("Escolha uma opção: ", 1, 5)

                if option == 1:
                    player.mostrar_status()
                    input("\nPressione Enter para continuar...")

                elif option == 2:
                    monstro_escolhido = copy.deepcopy(random.choice(self.monstros))
                    localizacao = random.choice(self.localizacoes)
                    combate = Combat(player, monstro_escolhido, localizacao)
                    combate.start()
                    salvar_player(player, player_id)
                    input("\nPressione Enter para continuar...")

                elif option == 3:
                    player.curar()
                    salvar_player(player, player_id)
                    input("\nPressione Enter para continuar...")

                elif option == 4:
                    player.inventario.mostrar_inventario()
                    input("\nPressione Enter para continuar...")

                elif option == 5:
                    print(f"See you later, {player.nome}")
                    jogando = False

                else:
                    print("Opção inválida.")