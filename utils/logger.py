import os
import csv
import requests


class Logger:

    def __init__(self, io_stream):
        self.io_stream = io_stream

        if self.io_stream == "console":
            cwd = os.getcwd()
            self.logs_output_path = cwd + "/files/logs.csv"

            if not os.path.exists(cwd + "/files"):
                os.makedirs(cwd + "/files")

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

        if self.io_stream == "console":
            with open(self.logs_output_path, "a", encoding="utf-8") as file:
                file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                file_writer.writerow([game_id, game_event, message])

        elif self.io_stream == "web":

            url = f"{os.getenv('DB_API_URI')}/cdg/log"

            requests.post(url, json={"game_id": game_id, "game_event": game_event, "message": message})

    def remove_logs(self):
        if self.io_stream == "console":
            os.remove(self.logs_output_path)
