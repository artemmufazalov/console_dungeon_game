from . errors import GameError


class GameController:
    """
    Класс контролера. Он отвечает за прием и первичную обработку команд пользователя
    """

    def __init__(self, game_engine):
        self.game_engine = game_engine

    def start(self):
        """Запуск приема команд от игрока"""

        active_tags = self.game_engine.get_tags()

        while self.game_engine.is_game_on:
            try:
                user_command = input("Введите команду: ").lower()

                if user_command.startswith("help"):
                    print(self.game_engine.help())

                elif user_command.startswith("print_field"):
                    self.game_engine.print_current_field()

                elif user_command.startswith("end_game"):

                    # Проверяем, действительно ли пользователь хочет закончить игру
                    def request_user_confirmation():
                        user_response = input("Вы уверены, что хотите завершить игру? (Да / Нет) ").lower()
                        if user_response == "yes" or user_response == "да":
                            print(self.game_engine.end_game())
                        elif user_response == "no" or user_response == "not" or user_response == "нет":
                            return
                        else:
                            print("Ваш ответ должен быть формата \"да\" или \"нет\".")
                            request_user_confirmation()

                    request_user_confirmation()

                elif user_command.startswith("info("):
                    arguments = list(map(lambda x: x.strip(), user_command[user_command.index("(") + 1: -1].split(",")))

                    if len(arguments) == 1:
                        if arguments[0] == "inv":
                            print(self.game_engine.inventory.info())
                        elif arguments[0] in active_tags:
                            print(self.game_engine.items_dict[arguments[0]].info())
                        else:
                            raise GameError("Переданный тэг не верен. Попробуйте запросить информацию по другому тэгу.")

                    elif len(arguments) == 2:
                        if arguments[0].isdigit() and arguments[1].isdigit():
                            arguments = list(map(int, arguments))

                            if arguments[0] > 8 or arguments[0] < 1 or arguments[1] > 8 or arguments[1] < 1:
                                raise GameError("Переданные координаты находятся за пределами игрового поля. "
                                                "Попробуйте изменить запрос.")
                            else:
                                print(self.game_engine.game_field[arguments[1] - 1][arguments[0] - 1].info())
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

                            print(self.game_engine.items_dict[tag].perform_action(action, [*arguments]))

                        else:
                            raise GameError(
                                "Вы не можете отдавать команды враждебным персонажам или неигровым объектам.")
                    else:
                        raise GameError("Введенная команда не корректна. Попробуйте изменить запрос.")

                else:
                    raise GameError("Введенная команда не корректна. Попробуйте изменить запрос.")

                print(self.game_engine.check_is_game_on())

            # Обрабатываем все игровые ошибки, возникшие в ходе игры
            except GameError as err:
                print(f"Операция не может быть выполнена. {err}\n")
