import os
import csv


class Logger:

    def __init__(self):
        cwd = os.getcwd()
        self.logs_output_path = cwd + "/logs/logs.csv"

    def log(self, game_id, game_event, message):
        """
        :param game_id: int, id текущей игры
        :param game_event: str, игровое событие
        :param message: str, описание события
        """

        with open(self.logs_output_path, "w", encoding="utf-8") as file:
            file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            file_writer.writerow(["Game_ID",
                                  "Game_Event",
                                  "Message"])

            file_writer.writerow([game_id, game_event, message])
