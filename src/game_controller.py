from . errors import GameError, GameEngineError


class GameController:
    """
    Класс контролера. Он отвечает за прием и первичную обработку команд пользователя
    """

    is_end_game_confirmation_request_pending = False

    def __init__(self, game_engine):
        self.game_engine = game_engine
        self.io_stream = ""
        self.action_result = ""

    def listen(self, io_stream="console"):
        """Запуск приема команд от игрока"""

        self.io_stream = io_stream

        if io_stream == "console":
            self.start_with_console()

        else:
            raise GameEngineError("Передан неверный поток ввода данных.")

    def start_with_console(self):
        """Запуск игры в режиме приема команд с консоли"""

        while self.game_engine.is_game_on:
            user_command = input("Введите команду: ").lower()
            print(self.listen_command(user_command))

    def _validate_end_game_confirmation_request(self, answer):
        if answer == "yes" or answer == "да":
            self.is_end_game_confirmation_request_pending = False
            return self.game_engine.end_game()
        elif answer == "no" or answer == "not" or answer == "нет":
            self.is_end_game_confirmation_request_pending = False
            return "Тогда продолжаем!"
        else:
            return "Ваш ответ должен быть формата \"да\" или \"нет\"."

    def listen_command(self, user_command):
        """Выполнение переданной команды"""
        active_tags = self.game_engine.get_tags()
        self.action_result = ""

        def append_result(line):
            self.action_result += line + "\n"

        try:

            if self.is_end_game_confirmation_request_pending:
                append_result(self._validate_end_game_confirmation_request(user_command))

            elif user_command.startswith("help"):
                append_result(self.game_engine.hepl())

            elif user_command.startswith("print_field"):
                append_result(self.game_engine.get_current_field_view())

            elif user_command.startswith("end_game"):
                # Проверяем, действительно ли пользователь хочет закончить игру
                self.is_end_game_confirmation_request_pending = True

                append_result("Вы уверены, что хотите завершить игру? (Да / Нет)")

            elif user_command == "repeat" or user_command == "repeat()":
                player_actions = self.game_engine.get_player_actions()
                if len(player_actions) == 0:
                    raise GameError("Нет команд, которые можно было бы повторить!")
                else:
                    character = player_actions[-1]["subject"]
                    action = player_actions[-1]["action"]
                    args = player_actions[-1]["args"]

                    if character.__class__.__name__[0].lower() not in self.game_engine.get_friendly_tags():
                        raise GameError(f"Команду невозможно повторить, возможно ваш \"{character.name}\" погиб!")

                    append_result(character.perform_action(action, args))

            elif user_command.startswith("info("):
                arguments = list(map(lambda x: x.strip(), user_command[user_command.index("(") + 1: -1].split(",")))

                if len(arguments) == 1:
                    if arguments[0] == "inv":
                        append_result(self.game_engine.inventory.info())
                    elif arguments[0] in active_tags:
                        append_result(self.game_engine.items_dict[arguments[0]].info())
                    else:
                        raise GameError("Переданный тэг не верен. Попробуйте запросить информацию по другому тэгу.")

                elif len(arguments) == 2:
                    if arguments[0].isdigit() and arguments[1].isdigit():
                        arguments = list(map(int, arguments))

                        if arguments[0] > 8 or arguments[0] < 1 or arguments[1] > 8 or arguments[1] < 1:
                            raise GameError("Переданные координаты находятся за пределами игрового поля. "
                                            "Попробуйте изменить запрос.")
                        else:
                            append_result(self.game_engine.game_field[arguments[1] - 1][arguments[0] - 1].info())
                    else:
                        raise GameError(
                            "Переданные аргументы не соответствуют требованиям. Попробуйте изменить запрос.")

            elif "." in user_command:
                if user_command[:user_command.index(".")] in active_tags:
                    tag = user_command[:user_command.index(".")]

                    if tag in self.game_engine.get_friendly_tags():
                        action = user_command[user_command.index(".") + 1: user_command.index("(")]
                        arguments = list(
                            map(lambda x: x.strip(), user_command[user_command.index("(") + 1: -1].split(",")))

                        append_result(self.game_engine.items_dict[tag].perform_action(action, [*arguments]))

                    else:
                        raise GameError(
                            "Вы не можете отдавать команды враждебным персонажам или неигровым объектам.")
                else:
                    raise GameError("Введенная команда не корректна. Попробуйте изменить запрос.")

            else:
                raise GameError("Введенная команда не корректна. Попробуйте изменить запрос.")

            append_result(self.game_engine.check_is_game_on())

            return self.action_result[:-1]

        # Обрабатываем все игровые ошибки, возникшие в ходе игры
        except GameError as err:
            return f"Операция не может быть выполнена. {err}\n"
