from . errors import GameError

# Базовые классы, от которых наследуются остальные


class GameItem:
    """
    Класс для игровых объектов, размещающихся на поле
    """
    def __init__(self, x_coord, y_coord):
        self.x = x_coord
        self.y = y_coord

    def info(self):
        """Возвращает строку с информацией об объекте"""
        pass


class SuperMovable:
    """
    Базовый класс для игровых объектов, способных перемещаться по игровому полю.
    От него наследуются другие базовые классы
    """

    def super_move(self, x, y, energy_cost, result):
        """
        Метод для перемещения объектов по полю\n
        :param x: int, координата x ячейки назначения
        :param y: int, координата y ячейки назначения
        :param energy_cost: int, количество энергии, необходимое для перемещения персонажа
        :param result: str, начальная строка, продолжая которую, формируется результат, который выводится игроку
        :return: str, строка, которая выводится игроку
        """

        # Для перемещения по полю, объекту необходимо взаимодействовать с игровым полем
        # Игровое поле записано в game_field в экземпляр класса Game_engine
        # Параметр game_engine присутствует у всех игровых персонажей,
        # которые наследуются у данного класса и могут перемещаться по полю
        if not hasattr(self, "game_engine"):
            raise GameError("У объекта нет прав взаимодействия с игровым полем.")

        if x > self.game_engine.get_width() or y > self.game_engine.get_length():
            raise GameError("Указанные координаты находятся за пределами игрового поля")

        # Получаем объект ячейки места назначения назначения
        game_spot = self.game_engine.game_field[y - 1][x - 1]

        # Проверяем занятость ячейки другими объектами
        if game_spot.get_spot_is_occupied():
            if game_spot.request_occupation_tag() != "t":
                raise GameError("Невозможно переместиться на ячейку, в ней уже находится другой объект.\n"
                                f"{game_spot.get_spot_owner().info()}")

            # Если в ячейке незащищенный сундук с сокровищами, то его можно открыть. 't' - тэг сундука с сокровищами
            elif game_spot.request_occupation_tag() == "t" and not game_spot.get_spot_is_protected():
                chest = game_spot.get_spot_owner()
                treasure = chest.open()

                # За добычу сокровища игроку начисляются игровые очки
                self.game_engine.add_score(self.game_engine.scores["chest"])

                result += "\nВ ячейке находится сундук. Открываем сундук..."
                result += f"\nВ сундуке {treasure.name}!"

                if "эликсир" in treasure.name.lower():
                    # Найденные эликсиры сохраняются в рюкзаке игрока и могут быть использованы позднее
                    result += f"\n{self.game_engine.inventory.add_item(treasure)}"
                else:
                    # Найденные предметы предназначены для определенного класса
                    # Если персонаж данного класса присутствует на поле,
                    # то предмет сразу используется, изменяя характеристики персонажа
                    if treasure.character_class.lower()[0] in self.game_engine.friendly_tags:
                        result += f"\n{treasure.use(self.game_engine.items_dict[treasure.character_class.lower()[0]])}"

                # Освобождаем ячейку
                game_spot.set_spot_owner(None)

                # Осуществляем непосредственно перемещение персонажа
                self._move(x, y, game_spot, energy_cost)

                return result

            # В ячейки, защищенные врагами перемещение невозможно
            elif game_spot.request_occupation_tag() == "t" and game_spot.get_spot_is_protected():
                result = "Ячейка защищена врагами! В ячейке находится сундук с сокровищем.\nВраги:"
                for enemy in self.game_engine.game_field[x-1][y-1].get_spot_protectors():
                    result += f"\n* {enemy.info()}"

                raise GameError(result)

        elif game_spot.get_spot_is_protected():
            result = "Ячейка защищена врагами!\nВраги:"
            for enemy in self.game_engine.game_field[x - 1][y - 1].get_spot_protectors():
                result += f"* {enemy.info()}"

            raise GameError(result)

        # Персонажи могут свободно перемещаться в ячейки,
        # свободные от врагов и других персонажей и не защищенные врагами
        elif game_spot.get_is_spot_free():
            self._move(x, y, game_spot, energy_cost)

            return result

    def _move(self, x, y, game_spot, energy_cost):
        """
        Внутренний метод для непосредственно изменения координат персонажа и расхода его энергии
        """
        game_spot.set_spot_owner(self)
        self.game_engine.game_field[self.y - 1][self.x - 1].set_spot_owner(None)
        self.x = x
        self.y = y
        self.energy = self.energy - energy_cost


class Movable(SuperMovable):
    """
    Класс для игровых объектов, способных перемещаться по игровому полю. От него наследуются классы игровых персонажей
    """

    def move(self, x, y):
        """
        Метод для перемещения игровых персонажей
        :param x: int, координата x места назначения
        :param y: int, координата y места назначения
        :return: str, строка, которая будет выведена пользователю
        """

        # По умолчанию, движение производится по катетам
        # Увы, игровые персонажи не самые умные ребята!
        total_distance = abs(self.x - x) + abs(self.y - y)

        # mec - характеристика персонажей, movement energy cost, расход энергии на единицу пройденного расстояния
        energy_cost = total_distance * self.mec

        if energy_cost > self.energy:
            raise GameError("Не хватает энергии на преодоление дистанции до указанной клетки.")
        else:
            if self.name == "Фея":
                result = f"{self.name} переместилась в ячейку ({x}, {y})."
            else:
                result = f"{self.name} переместился в ячейку ({x}, {y})."

            return SuperMovable.super_move(self, x, y, energy_cost, result)


class Flyable(SuperMovable):
    """
    Класс для игровых объектов, способных летать по игровому полю. От него наследуются классы игровых персонажей
    """

    default_energy_cost = 5

    def fly(self, x, y):
        """
        Метод для перемещения игровых персонажей. Расходует фиксированное количество энергии
        :param x: int, координата x места назначения
        :param y: int, координата y места назначения
        :return: str, строка, которая будет выведена пользователю
        """

        if self.default_energy_cost > self.energy:
            raise GameError("Не хватает энергии на преодоление дистанции до указанной клетки.")
        else:
            # Так как использовать метод планируется только для феи, то вывод только для женского пола
            result = f"{self.name} перелетела в ячейку ({x}, {y})."
            return SuperMovable.super_move(self, x, y, self.default_energy_cost, result)
