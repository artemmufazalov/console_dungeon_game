import os
import csv
import requests


class Logger:

    def __init__(self):
        if os.getenv("IO_STREAM") == "console":
            cwd = os.getcwd()
            self.logs_output_path = cwd + "/files/logs.csv"

            if not os.path.isfile(self.logs_output_path):
                with open(self.logs_output_path, "w", encoding="utf-8") as file:
                    file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                    file_writer.writerow(["Game_ID", "Game_Event", "Message"])

    def log(self, game_id, game_event, message):
        """
        :param game_id: int, id текущей игры
        :param game_event: str, игровое событие
        :param message: str, описание события
        """

        io_stream = os.getenv("IO_STREAM")

        if io_stream == "console":
            with open(self.logs_output_path, "a", encoding="utf-8") as file:
                file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                file_writer.writerow([game_id, game_event, message])

        elif io_stream == "web":

            url = f"{os.getenv('DB_API_URI')}/cdg/log"

            requests.post(url, json={"game_id": game_id, "game_event": game_event, "message": message})

    def remove_logs(self):
        if os.getenv("IO_STREAM") == "console":
            os.remove(self.logs_output_path)
