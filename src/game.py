import os

from . game_engine import GameEngine
from . game_controller import GameController
from utils.logger import Logger
from utils.helpers import generate_game_id


class Game:
    """Игра Console Dungeon"""

    is_on = False

    def __init__(self):

        self.is_on = True

        # Инициализируем игровой движок и контроллер
        self.game_id = generate_game_id()

        logger = Logger()

        self.game_engine = GameEngine(self, self.game_id, logger)
        self.game_controller = GameController(self.game_engine)

    def set_off(self):
        self.is_on = False

    def start(self):
        """Запускает игровой движок и контроллер для приема команд"""
        io_stream = os.getenv("IO_STREAM", "console")

        result = self.game_engine.start_game()

        if io_stream == "console":
            print(result)

        self.game_controller.listen(io_stream=io_stream)

        return result
