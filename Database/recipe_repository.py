from Database.connection import conectar
from Entities.recipe import Recipe


def criar_receita(item_resultado_id: int, quantidade_produzida: int, nivel_crafting_minimo: int,
                   tipo_estacao: str, ingredientes: list[tuple[int, int]]) -> int:
    """Cria uma receita e seus ingredientes.

    ingredientes: lista de tuplas (item_id, quantidade_necessaria)
    """
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO recipes (item_resultado_id, quantidade_produzida, nivel_crafting_minimo, tipo_estacao)
        VALUES (%s, %s, %s, %s)
        RETURNING id
    """, (item_resultado_id, quantidade_produzida, nivel_crafting_minimo, tipo_estacao))
    recipe_id = cursor.fetchone()[0]

    for item_id, quantidade_necessaria in ingredientes:
        cursor.execute("""
            INSERT INTO recipe_ingredients (recipe_id, item_id, quantidade_necessaria)
            VALUES (%s, %s, %s)
        """, (recipe_id, item_id, quantidade_necessaria))

    conexao.commit()
    cursor.close()
    conexao.close()
    return recipe_id


def carregar_receitas(itens: dict) -> dict:
    """Carrega todas as receitas com seus ingredientes, indexadas por item_resultado_id.

    `itens`: dict {item_id: Item} já carregado (mesmo dict que item_repository.carregar_itens()
    retorna), usado para resolver item_resultado_id e os ingredientes em objetos Item de verdade.

    Um mesmo item_resultado_id pode ter mais de uma receita (rotas alternativas de
    crafting pro mesmo item), por isso o valor é sempre uma LISTA de objetos Recipe:
    { item_resultado_id: [Recipe, Recipe, ...], ... }

    Receitas cujo item_resultado ou algum ingrediente não seja encontrado em `itens`
    são ignoradas (com um aviso), em vez de quebrar o carregamento inteiro.
    """
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, item_resultado_id, quantidade_produzida, nivel_crafting_minimo, tipo_estacao
        FROM recipes
    """)
    linhas_receitas = cursor.fetchall()

    # carrega todos os ingredientes de uma vez (evita N+1 queries) e agrupa por recipe_id
    cursor.execute("""
        SELECT recipe_id, item_id, quantidade_necessaria FROM recipe_ingredients
    """)
    linhas_ingredientes = cursor.fetchall()

    cursor.close()
    conexao.close()

    ingredientes_por_receita = {}
    for recipe_id, item_id, quantidade in linhas_ingredientes:
        ingredientes_por_receita.setdefault(recipe_id, []).append({
            "item_id": item_id,
            "quantidade": quantidade
        })

    receitas = {}
    for recipe_id, item_resultado_id, quantidade_produzida, nivel_crafting_minimo, tipo_estacao in linhas_receitas:
        item_resultado = itens.get(item_resultado_id)
        if item_resultado is None:
            print(f"Receita {recipe_id}: item_resultado_id {item_resultado_id} não encontrado, pulando.")
            continue

        ingredientes = []
        ingrediente_faltando = False
        for ingrediente in ingredientes_por_receita.get(recipe_id, []):
            item_ingrediente = itens.get(ingrediente["item_id"])
            if item_ingrediente is None:
                print(f"Receita {recipe_id}: ingrediente item_id {ingrediente['item_id']} não encontrado, pulando receita.")
                ingrediente_faltando = True
                break
            ingredientes.append({"item": item_ingrediente, "quantidade": ingrediente["quantidade"]})

        if ingrediente_faltando:
            continue

        receita = Recipe(
            id=recipe_id,
            item_resultado=item_resultado,
            quantidade_produzida=quantidade_produzida,
            nivel_crafting_minimo=nivel_crafting_minimo,
            tipo_estacao=tipo_estacao,
            ingredientes=ingredientes
        )
        receitas.setdefault(item_resultado_id, []).append(receita)

    return receitas


def buscar_receitas_por_item(item_resultado_id: int, itens: dict) -> list:
    """Retorna todas as receitas que produzem esse item (pode ser mais de uma)."""
    return carregar_receitas(itens).get(item_resultado_id, [])