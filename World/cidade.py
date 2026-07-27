class Cidade:
    def __init__(self, id: int, nome: str, regiao: str, descricao: str) -> None:
        self.id = id
        self.nome = nome
        self.regiao = regiao
        self.descricao = descricao

    def __str__(self):
        return f"{self.nome} ({self.regiao})"


class Bancada:
    def __init__(self, id: int, tipo: str) -> None:
        self.id = id
        self.tipo = tipo

    def __str__(self):
        return self.tipo