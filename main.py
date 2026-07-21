from Database.seed import popular_items, popular_localizacoes, popular_monstros
from Systems.game_manager import Game

# Popula o banco automaticamente (só insere o que ainda não existe, graças à checagem de duplicata)
popular_items()
popular_localizacoes()
popular_monstros()


game = Game()
game.run()