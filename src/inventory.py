from . errors import GameError


class Inventory:
    """Класс рюкзака игрока"""

    _inventory = []

    def del_item(self, item):
        """Удаляет переданный предмет из рюкзака"""
        self._inventory.remove(item)

    def add_item(self, item):
        """Добавляет переданный предмет в рюкзак"""
        self._inventory.append(item)

        return f"Предмет {item.name} был добавлен в рюкзак."

    def get_potion(self, tag):
        """
        Возвращает объект зелья, соответствующий переданному тэгу, если он есть в рюкзаке\n
        :param tag: str, "health" для эликсиров здоровья, "energy" для эликсиров энергии
        """

        if "health" in tag:
            for item in self._inventory:
                if "health" in item.__class__.__name__.lower():
                    return item

            raise GameError("У вас закончились зелья здоровья!")

        elif "energy" in tag:
            for item in self._inventory:
                if "energy" in item.__class__.__name__.lower():
                    return item

            raise GameError("У вас закончились зелья энергии'!")

        else:
            raise GameError("Введено несуществующее описание зелья.")

    def info(self):
        """Возвращает строку с информацией о содержимом рюкзака"""

        items_count = len(self._inventory)
        if len(self._inventory) == 0:
            return "Ваш рюкзак пуст."
        else:
            if items_count == 1:
                result = f"В вашем рюкзаке лежит 1 предмет."
            elif 5 > items_count > 1:
                result = f"В вашем рюкзаке лежит {items_count} предмета."
            else:
                result = f"В вашем рюкзаке лежит {items_count} предметов."

            for treasure in self._inventory:
                result += f"\n* {treasure.info()}"

            return result
