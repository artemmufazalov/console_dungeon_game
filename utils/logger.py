import os
import csv


class Logger:

    def __init__(self):
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

        with open(self.logs_output_path, "a", encoding="utf-8") as file:
            file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            file_writer.writerow([game_id, game_event, message])

    def remove_logs(self):
        os.remove(self.logs_output_path)
