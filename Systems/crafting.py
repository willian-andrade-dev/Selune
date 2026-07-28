import random
from collections import Counter
from dataclasses import dataclass
from typing import TYPE_CHECKING

from Database.inventory_repository import remover_item_inventario, adicionar_item_inventario
from Database.crafting_skill_repository import atualizar_crafting_skill
from Database.city_repository import carregar_bancadas

if TYPE_CHECKING:
    from Entities.player import Player
    from Entities.recipe import Recipe
    from World.cidade import Cidade


@dataclass
class ResultadoCraft:
    """Retorno de craftar() — sem nenhum print embutido, pra poder ser consumido
    tanto pelo console (print direto) quanto por um front-end assíncrono (Discord:
    embed/reply), sem duplicar a regra de negócio em cada um."""
    sucesso: bool
    mensagem: str
    quantidade_produzida: int = 0
    subiu_nivel_crafting: bool = False

def listar_todas_receitas(receitas_por_item: dict) -> list:
    """Achata o dict {item_resultado_id: [Recipe, ...]} numa lista única.
    Usado pra exibir o catálogo completo de crafting, sem filtro nenhum."""
    todas = []
    for receitas_do_item in receitas_por_item.values():
        todas.extend(receitas_do_item)
    return todas


def listar_receitas_craftaveis(player: 'Player', receitas_por_item: dict) -> list:
    """Retorna só as receitas para as quais o player já tem ingredientes suficientes
    agora. Não checa nível de crafting nem estação aqui de propósito — é um filtro
    rápido de 'o que dá pra fazer com o que eu tenho', a checagem completa acontece
    em craftar()."""
    contagem_inventario = Counter(item.nome for item in player.inventario.itens)
    return [
        receita
        for receitas_do_item in receitas_por_item.values()
        for receita in receitas_do_item
        if _tem_ingredientes_suficientes(receita, contagem_inventario)
    ]


def _tem_ingredientes_suficientes(receita: 'Recipe', contagem_inventario: Counter) -> bool:
    for ingrediente in receita.ingredientes:
        nome = ingrediente["item"].nome
        quantidade_necessaria = ingrediente["quantidade"]
        if contagem_inventario.get(nome, 0) < quantidade_necessaria:
            return False
    return True


def _chance_dobrar(nivel_crafting: int) -> float:
    """Chance mínima de dobrar a quantidade produzida, escalando com o nível de
    crafting. Começa baixa e cresce devagar de propósito — é um bônus ocasional,
    não deve virar a regra. Valores ajustáveis."""
    return min(0.01 + nivel_crafting * 0.002, 0.25)  # cap em 25%


def _xp_por_craft(receita: 'Recipe') -> int:
    """XP de crafting ganho por craft bem-sucedido, escalando com o nível mínimo
    exigido pela receita. Valor ajustável."""
    return max(5, receita.nivel_crafting_minimo * 2)


def craftar(player: 'Player', receita: 'Recipe', cidade: 'Cidade') -> ResultadoCraft:
    """Executa o crafting de uma receita: valida nível, bancada e ingredientes,
    consome os ingredientes, produz o(s) item(ns) (com chance de dobrar) e concede
    xp de crafting. Não faz nenhum print — quem chamar decide como exibir o
    resultado (console, embed do Discord, etc.)."""

    if not receita.nivel_suficiente(player):
        return ResultadoCraft(
            sucesso=False,
            mensagem=f"Você precisa de nível de crafting {receita.nivel_crafting_minimo} para "
                      f"{receita.item_resultado.nome} (seu nível: {player.crafting_skill.nivel})."
        )

    bancadas_da_cidade = [bancada.tipo for bancada in carregar_bancadas(cidade.id)]
    if receita.tipo_estacao not in bancadas_da_cidade:
        return ResultadoCraft(
            sucesso=False,
            mensagem=f"Você precisa de uma bancada de {receita.tipo_estacao} para craftar "
                     f"{receita.item_resultado.nome} (não disponível em {cidade.nome})."
        )

    contagem_inventario = Counter(item.nome for item in player.inventario.itens)
    if not _tem_ingredientes_suficientes(receita, contagem_inventario):
        return ResultadoCraft(
            sucesso=False,
            mensagem=f"Ingredientes insuficientes para craftar {receita.item_resultado.nome}."
        )

    # consome os ingredientes (inventário em memória + banco)
    for ingrediente in receita.ingredientes:
        item_ingrediente = ingrediente["item"]
        for _ in range(ingrediente["quantidade"]):
            player.inventario.remover_item(item_ingrediente)
        remover_item_inventario(player.id, item_ingrediente.id, ingrediente["quantidade"])

    # chance de dobrar a produção, escalando com o nível de crafting
    dobrou = random.random() < _chance_dobrar(player.crafting_skill.nivel)
    quantidade_final = receita.quantidade_produzida * 2 if dobrou else receita.quantidade_produzida

    for _ in range(quantidade_final):
        player.inventario.adicionar_item(receita.item_resultado)
    adicionar_item_inventario(player.id, receita.item_resultado.id, quantidade_final)

    xp_ganho = _xp_por_craft(receita)
    subiu_nivel = player.crafting_skill.ganhar_xp(xp_ganho)
    atualizar_crafting_skill(player.id, player.crafting_skill.nivel, player.crafting_skill.xp)

    mensagem = f"{player.nome} craftou {quantidade_final}x {receita.item_resultado.nome}!"
    if dobrou:
        mensagem += " Inspiração no trabalho! A quantidade produzida dobrou."
    if subiu_nivel:
        mensagem += f" Sua habilidade de crafting subiu para o nível {player.crafting_skill.nivel}!"

    return ResultadoCraft(
        sucesso=True,
        mensagem=mensagem,
        quantidade_produzida=quantidade_final,
        subiu_nivel_crafting=subiu_nivel
    )


# ==========================================
# MENU DE CONSOLE — usa input()/print() direto; será substituído por
# handlers assíncronos (Views/Select do discord.py) na integração com o bot.
# Não deve conter regra de negócio nova, só chamar as funções acima.
# ==========================================

def _ler_opcao(minimo: int, maximo: int) -> int:
    """Lê um número inteiro do usuário, validando o intervalo. Repete até ser válido."""
    while True:
        entrada = input(f"Escolha uma opção ({minimo}-{maximo}): ")
        if entrada.isdigit() and minimo <= int(entrada) <= maximo:
            return int(entrada)
        print("Opção inválida, tente novamente.")


def _formatar_ingredientes(receita: 'Recipe', contagem_inventario: Counter) -> str:
    """Monta uma linha por ingrediente mostrando quanto o player tem vs. quanto precisa."""
    linhas = []
    for ingrediente in receita.ingredientes:
        nome = ingrediente["item"].nome
        necessario = ingrediente["quantidade"]
        tem = contagem_inventario.get(nome, 0)
        marca = "✓" if tem >= necessario else "✗"
        linhas.append(f"      {marca} {nome} ({tem}/{necessario})")
    return "\n".join(linhas)


def _escolher_e_craftar(player: 'Player', receitas: list, cidade: 'Cidade') -> None:
    """Mostra uma lista de receitas já filtrada, deixa o player escolher uma e craftar."""
    contagem_inventario = Counter(item.nome for item in player.inventario.itens)

    print("\n==== RECEITAS ====")
    for i, receita in enumerate(receitas, start=1):
        print(f"{i} - {receita}")
        print(_formatar_ingredientes(receita, contagem_inventario))
    print(f"{len(receitas) + 1} - Voltar")

    escolha = _ler_opcao(1, len(receitas) + 1)
    if escolha == len(receitas) + 1:
        return

    receita_escolhida = receitas[escolha - 1]
    resultado = craftar(player, receita_escolhida, cidade)
    print(resultado.mensagem)


def menu_crafting(player: 'Player', receitas_por_item: dict, cidade: 'Cidade') -> None:
    """Menu principal de crafting: escolher ver o catálogo completo ou só o que dá
    pra craftar agora com os itens em mãos."""
    while True:
        print("\n==== CRAFTING ====")
        print(f"Bancadas em {cidade.nome}: {', '.join(b.tipo for b in carregar_bancadas(cidade.id))}")
        print("1 - Ver todas as receitas")
        print("2 - Ver receitas craftáveis (com o que você tem agora)")
        print("3 - Sair")
        escolha = _ler_opcao(1, 3)

        if escolha == 3:
            return

        if escolha == 1:
            receitas = listar_todas_receitas(receitas_por_item)
        else:
            receitas = listar_receitas_craftaveis(player, receitas_por_item)

        if not receitas:
            print("Nenhuma receita encontrada.")
            continue

        _escolher_e_craftar(player, receitas, cidade)