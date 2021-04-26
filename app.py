import os
from flask import Flask

from src.game import Game
from server.server import App

if os.getenv("IO_STREAM") == "web":
    my_app = App()

    app = Flask(__name__)

    app.after_request(my_app.after_request)

    @app.route('/')
    def welcome(): return "Welcome to CDG api"

    @app.route('/init', methods=['GET'])
    def init_game(): return my_app.init_game()

    @app.route('/perform', methods=['POST'])
    def perform_action(): return my_app.perform_action()

    @app.route('/perform', methods=['POST'])
    def end_game(): return my_app.end_game()

    if __name__ == "__main__":
        app.run(port=int(os.getenv("PORT", 5000)), host='0.0.0.0')

else:
    game = Game()
    game.start()
