import json
import os
import requests
import random


def generate_game_id():
    io_stream = os.getenv("IO_STREAM")

    game_id = int()

    try:
        if io_stream == "console":
            path = os.getcwd() + "/files/meta.json"

            if not os.path.isfile(path):
                with open(path, "w", encoding="utf-8") as file:
                    json.dump({"last_game_id": 0}, file)

            with open(path) as file_to_read:
                data = json.load(file_to_read)

                data["last_game_id"] += 1
                game_id = data["last_game_id"]

                with open(path, "w") as file_to_write:
                    json.dump(data, file_to_write)

        elif io_stream == "web":
            url = f"{os.getenv('DB_API_URI')}/cdg/gameid"
            response = requests.get(url)
            if int(response.status_code) == 200:
                game_id = int(response.json()["game_id"])
            else:
                game_id = random.randint(1, 1000000)

    except BaseException:
        game_id = random.randint(1, 1000000)

    return game_id
