from Database.connection import conectar
from World.location import Localização

def criar_localizacao(nome: str, dificuldade: int, regiao: str) -> int:
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT id FROM locations WHERE nome = %s", (nome,))
    existe = cursor.fetchone()

    if existe:
        print(f"{nome} já existe no banco, pulando.")
        cursor.close()
        conexao.close()
        return existe[0]

    cursor.execute("""
        INSERT INTO locations (nome, dificuldade,regiao)
        VALUES (%s, %s, %s)
        RETURNING id
    """, (nome, dificuldade, regiao))

    location_id = cursor.fetchone()[0]

    conexao.commit()
    cursor.close()
    conexao.close()

    return location_id

def carregar_localizacoes() -> list:
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome, dificuldade, regiao FROM locations")
    linhas = cursor.fetchall()
    cursor.close()
    conexao.close()

    localizacoes = []
    for linha in linhas:
        id, nome, dificuldade, regiao = linha
        localizacao = Localização(nome, dificuldade, regiao) # variavel no singular
        localizacoes.append(localizacao) # adiciona na lista, sem apagar as outras
    return localizacoes