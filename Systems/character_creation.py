from Entities.player import Player
from Database.player_repository import criar_player, salvar_player
from Database.inventory_repository import adicionar_item_inventario

EQUIPAMENTO_INICIAL = {
    'Guerreiro': 'Espada de Treino',
    'Mago': 'Cajado Iniciante',
    'Arqueiro': 'Arco Curto',
    'Clérigo': 'Talismã Sagrado',
}

class CharacterCreation:
    def __init__(self, itens: dict) -> None:
        self.itens = itens

    def buscar_item_por_nome(self, nome: str):
        for item in self.itens.values():
            if item.nome == nome:
                return item
        return None

    def criar_personagem(self, nome: str, classe_escolhida) -> tuple:
        player = Player(
            nome, classe_escolhida.hp_base, classe_escolhida.mana_base, 100, 0, 1,
            classe_escolhida.ataque_base, classe_escolhida.armadura_base, classe_escolhida.id,
            classe_escolhida.hp_regen_base, classe_escolhida.hp_regen_por_nivel,
            classe_escolhida.mana_regen_base, classe_escolhida.mana_regen_por_nivel
        )
        player_id = criar_player(
            nome, classe_escolhida.hp_base, classe_escolhida.hp_base, classe_escolhida.mana_base,
            100, 0, player.xp_para_upar, 1, classe_escolhida.ataque_base, classe_escolhida.ataque_base,
            classe_escolhida.armadura_base, classe_escolhida.armadura_base, classe_escolhida.id
        )
        player.id = player_id
        self._dar_equipamento_inicial(player, classe_escolhida, player_id)
        salvar_player(player, player_id)
        return player, player_id

    def _dar_equipamento_inicial(self, player, classe_escolhida, player_id) -> None:
        nome_arma = EQUIPAMENTO_INICIAL.get(classe_escolhida.nome)
        arma = self.buscar_item_por_nome(nome_arma)
        armadura = self.buscar_item_por_nome('Túnica de Linho')
        pocao_cura = self.buscar_item_por_nome('Poção de Cura Menor')

        for item, quantidade in [(arma, 1), (armadura, 1), (pocao_cura, 5)]:
            if item is None:
                continue
            for _ in range(quantidade):
                player.inventario.adicionar_item(item)
            adicionar_item_inventario(player_id, item.id, quantidade)

        if arma is not None:
            arma.use(player)
        if armadura is not None:
            armadura.use(player)