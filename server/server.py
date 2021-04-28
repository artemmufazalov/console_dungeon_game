from flask import Flask, request, jsonify
from datetime import datetime

from src.game import Game


class App:
    active_games = {}
    _expiration = 5 * 60 * 60

    def __init__(self):
        pass

    def after_request(self, response):
        self._delete_invalid_games()

        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")

        return response

    def init_game(self):
        try:
            game = Game()
            self._add_new_game(game)
            game_id = game.game_id
            response_content = game.start()

            return jsonify({
                "game_id": game_id,
                "response_content": response_content,
            }), 200

        except Exception as err:
            return jsonify({
                "response_content": f"Some error occurred! Request could not be completed",
                "error": str(err)
            }), 500

    def perform_action(self):
        data = request.json

        command = data["command"]
        game_id = data["game_id"]

        if command and game_id:
            try:
                game = self._get_game_by_id(game_id)
                result = game.game_controller.listen_command(command)
                is_on = game.is_on

                return jsonify({
                    "game_id": game_id,
                    "response_content": result,
                    "is_on": is_on
                }), 200

            except Exception as err:
                return jsonify({
                    "response_content": f"Some error occurred! Request could not be completed",
                    "error": str(err)
                }), 500
        else:
            return jsonify({
                "response_content": "Was provided invalid arguments!",
            }), 403

    def end_game(self):
        game_id = int(request.form.get("game_id"))

        if game_id:
            try:
                game = self._get_game_by_id(game_id)
                result = game.game_engine.end_game()

                return jsonify({
                    "game_id": game_id,
                    "response_content": result,
                    "is_on": False
                }), 200

            except Exception as err:
                return jsonify({
                    "response_content": f"Some error occurred! Request could not be completed",
                    "error": str(err)
                }), 500
        else:
            return jsonify({
                "response_content": "Was provided invalid arguments!",
            }), 403

    def _add_new_game(self, game):
        self.active_games[str(game.game_id)] = {
            "game": game,
            "game_id": game.game_id,
            "start_time": int(datetime.now().timestamp())
        }

    def _get_game_by_id(self, game_id):
        if str(game_id) in self.active_games:
            return self.active_games[str(game_id)]["game"]
        else:
            raise Exception(f"Игра с ID {game_id} не была найдена!")

    def _end_game_with_id(self, game_id):
        for key in list(self.active_games.keys()):
            game = self.active_games[key]["game"]
            if game.game_id == str(game_id):
                game.is_on = False

    def _delete_invalid_games(self):
        def _is_expired(game_obj):
            return (int(datetime.now().timestamp())
                    - self.active_games[str(game_obj.game_id)]["start_time"]) > App._expiration

        for key in list(self.active_games.keys()):
            game = self.active_games[key]["game"]

            if not game.is_on:
                self.active_games.pop(key, None)

            elif _is_expired(game):
                self.active_games.pop(key, None)
