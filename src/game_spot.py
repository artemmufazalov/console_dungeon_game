class GameSpot:
    """Класс ячейки игрового поля"""

    def __init__(self, x_coord, y_coord, is_occupied, spot_owner, is_protected, protectors):
        """
        :param x_coord: int, координата x ячейки
        :param y_coord: int, координата y ячейки
        :param is_occupied: bool, True, если в ячейке есть объект
        :param spot_owner: object, объект, расположенный в ячейке
        :param is_protected: bool, True, если ячейка защищена врагом
        :param protectors: [objects], список врагов, защищающих ячейку
        """

        self.x = x_coord
        self.y = y_coord
        self._is_occupied = is_occupied
        self._owner = spot_owner
        self._is_protected = is_protected
        self._protectors = [*protectors]

    def get_is_spot_free(self):
        """Возвращает статус ячейки. True, если в ячейке нет объекта и она не защищена врагами"""
        return not self._is_protected and not self._is_occupied

    def get_spot_is_occupied(self):
        """Возвращает статус ячейки. True, если в ячейке находится объект"""
        return self._is_occupied

    def get_spot_is_protected(self):
        """Возвращает статус ячейки. True, если ячейка защищена врагами"""
        return self._is_protected

    def get_spot_owner(self):
        """Возвращает объект, расположенный в ячейке"""
        return self._owner

    def get_spot_protectors(self):
        """Возвращает врагов, защищающих клетку"""
        return self._protectors

    def change_spot_owner(self, new_owner):
        """Изменяет объект, расположенный в ячейке"""
        self._owner = new_owner
        self._is_occupied = True

    def loose_spot_protection(self, enemy_id):
        """
        Удаляет врага с переданным id из списка защитников ячейки\n
        :param enemy_id: int, id врага
        """

        self._protectors = list(filter(lambda protector: protector.id != enemy_id, self._protectors))
        if len(self._protectors) == 0:
            self._is_protected = False

    def set_spot_protector(self, protector):
        """Добавляет защитника для ячейки"""

        self._protectors.append(protector)
        self._is_protected = True

    def set_spot_owner(self, new_owner):
        """Устанавливает нового владельца ячейки - находящийся в ячейке объект"""

        if new_owner is None:
            self._is_occupied = False
        else:
            self._owner = new_owner
            self._is_occupied = True

    def request_occupation_tag(self):
        """Возвращает тэг владельца ячейки"""

        if self._is_occupied:
            response = self._owner.get_tag()
        elif self._is_protected:
            response = "#"
        else:
            response = "*"

        return response

    def info(self):
        """Возвращает строку с информацией о ячейке"""

        data = ""

        if self._is_protected:
            if len(self._protectors) == 1:
                data += f"Данная ячейка защищается врагом.\n{self._protectors[0].info()}"
            else:
                data += f"Данная ячейка защищается врагами."
                for enemy in self._protectors:
                    data += f"\n{enemy.info()}"

        elif self._is_occupied:
            data += f"Данная ячейка занята. "
            if type(self._owner) == "Treasure":
                data += f"В данной ячейке находится сундук с сокровищем."
            elif "PlayableCharacter" in list(map(lambda x: x.__name__, self._owner.__class__.__bases__)):
                data += f"В данной ячейке находится игровой персонаж.\n{self._owner.info()}"
            else:
                data += f"В данной ячейке находится враг.\n{self._owner.info()}"

        else:
            data += "Ячейка пуста."

        return f"Клетка ({self.x},{self.y}): \n{data}"
