import os

from . game_engine import GameEngine
from . game_controller import GameController
from utils.logger import Logger
from utils.helpers import generate_game_id


class Game:
    """Игра Console Dungeon"""

    def __init__(self):

        # Инициализируем игровой движок и контроллер
        self.game_id = generate_game_id()

        logger = Logger()

        self.game_engine = GameEngine(self.game_id, logger)
        self.game_controller = GameController(self.game_engine)

    def start(self):
        """Запускает игровой движок и контроллер для приема команд"""
        io_stream = os.getenv("IO_STREAM", "console")

        self.game_engine.start_game()
        self.game_controller.listen(io_stream=io_stream)
