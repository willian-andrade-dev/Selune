from Database.connection import conectar


def carregar_tipos_bancada(cidade_id: int) -> list[str]:
    """Retorna os tipos de bancada disponíveis numa cidade (ex: ['Ferraria', 'Alquimia',
    'Joalheria', 'Arcanismo']). Toda cidade tem as 4 por causa do trigger de criação,
    mas a consulta fica explícita mesmo assim (não assume isso na regra de negócio)."""
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT tipo FROM bancadas WHERE cidade_id = %s
    """, (cidade_id,))
    linhas = cursor.fetchall()

    cursor.close()
    conexao.close()

    return [tipo for (tipo,) in linhas]