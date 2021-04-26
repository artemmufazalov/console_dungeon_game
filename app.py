import os

from src.game import Game
from server.server import App


if os.getenv("IO_STREAM") == "web":
    app = App()
    app.run()
else:
    game = Game()
    game.start()
