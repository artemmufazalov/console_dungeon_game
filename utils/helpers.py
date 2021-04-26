import json
import os


def generate_game_id():
    path = os.getcwd() + "/files/meta.json"

    if not os.path.isfile(path):
        with open(path, "w", encoding="utf-8") as file:
            json.dump({"last_game_id": 0}, file)

    game_id = int()

    with open(path) as file_to_read:
        data = json.load(file_to_read)

        data["last_game_id"] += 1
        game_id = data["last_game_id"]

        with open(path, "w") as file_to_write:
            json.dump(data, file_to_write)

    return game_id
