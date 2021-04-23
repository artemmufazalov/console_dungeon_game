import os

from . game_engine import GameEngine
from . game_controller import GameController


class Game:
    """Игра Console Dungeon"""

    games_count = 0

    def __init__(self):

        # Инициализируем игровой движок и контроллер
        Game.games_count += 1

        self.game_id = Game.games_count
        self.game_engine = GameEngine()
        self.game_controller = GameController(self.game_engine)

    def start(self):
        """Запускает игровой движок и контроллер для приема команд"""
        io_stream = os.getenv("IO_STREAM", "console")

        self.game_engine.start_game()
        self.game_controller.listen(io_stream=io_stream)
