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

itens = carregar_itens()
monstros = carregar_monstros(itens)
localizacoes = carregar_localizacoes()

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

rpg_program = True
while rpg_program:
    print("1 - Criar personagem novo")
    print("2 - Carregar personagem existente")
    print("3 - Log Out")
    opcao_inicial = int(input("Escolha uma opção: "))

    if opcao_inicial == 1:
        nome = input("Nome do personagem: ")
        player_id = criar_player(nome, 20, 20, 5, 15, 0, 75, 1, 10, 10, 0, 0)
        player = Player(nome, 20, 5, 15, 0, 1, 10, 0)
        player.id = player_id
        print(f"Personagem {nome} criado com ID {player_id}!")

    elif opcao_inicial == 2:
        player_id = int(input("Digite o ID do seu personagem: "))
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
        limpar_tela()
        print("1 - Mostrar status")
        print("2 - Atacar criatura")
        print("3 - Se curar")
        print("4 - Mostrar inventário")
        print("5 - Log Out")
        option = int(input("Escolha uma opção: "))

        if option == 1:
            player.Show_status()
            input("\nPressione Enter para continuar...")

        elif option == 2:
            monstro_escolhido = copy.deepcopy(random.choice(monstros))
            localizacao = random.choice(localizacoes)
            combate = Combat(player, monstro_escolhido, localizacao)
            combate.start()
            salvar_player(player, player_id)
            input("\nPressione Enter para continuar...")

        elif option == 3:
            player.Heal()
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