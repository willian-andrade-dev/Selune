import random


def todos_monstros(monstros_disponiveis) -> list:
    """Normaliza uma coleção de monstros (dict ou list) para uma lista."""
    if isinstance(monstros_disponiveis, dict):
        return list(monstros_disponiveis.values())
    return list(monstros_disponiveis)


def monstros_da_localizacao(monstros_disponiveis, localizacao) -> list:
    return [m for m in todos_monstros(monstros_disponiveis) if localizacao.id in m.location_ids]


def sortear_grupo(monstros_disponiveis, nomes_preferidos: list[str], localizacao) -> list:
    monstros_locais = monstros_da_localizacao(monstros_disponiveis, localizacao)
    if not monstros_locais:
        return []

    candidatos = [m for m in monstros_locais if m.nome in nomes_preferidos]
    if not candidatos:
        # a lista fixa não cobre o bioma dessa localização — usa os monstros nativos dela
        candidatos = monstros_locais

    tamanho = random.randint(2, 3)
    return random.choices(candidatos, k=tamanho)  # com repetição: "2 Bandidos Novatos" é válido