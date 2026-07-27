from Database.connection import conectar
from World.cidade import Cidade, Bancada


def carregar_cidades() -> list:
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome, regiao, descricao FROM cidades ORDER BY nome")
    linhas = cursor.fetchall()
    cursor.close()
    conexao.close()

    return [Cidade(id, nome, regiao, descricao) for id, nome, regiao, descricao in linhas]


def carregar_bancadas(cidade_id: int) -> list:
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, tipo FROM bancadas WHERE cidade_id = %s ORDER BY tipo", (cidade_id,))
    linhas = cursor.fetchall()
    cursor.close()
    conexao.close()

    return [Bancada(id, tipo) for id, tipo in linhas]