from . game_engine import GameEngine
from . game_controller import GameController


class Game:
    """Игра Console Dungeon"""

    def __init__(self):

        # Инициализируем игровой движок и контроллер
        self.game_engine = GameEngine()
        self.game_controller = GameController(self.game_engine)

    def start(self):
        """Запускает игровой движок и контроллер для приема команд"""
        self.game_engine.start_game()
        self.game_controller.listen()
