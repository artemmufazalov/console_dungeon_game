import random

from . errors import GameError
from . helpers import en_ru_features_dict, get_random_list_element
from . base_classes import GameItem


class Treasure:
    """Класс игровых предметов"""

    name = "Сокровище"
    character_class = "any"
    features_for_update = {}

    def use(self, character):
        """
        Использование предмет для улучшения характеристик персонажа\n
        :param character: PlayableCharacter, игровой персонаж, наследник класса PlayableCharacter
        """

        if self.character_class != "any" and character.__class__.__name__ != self.character_class:
            raise GameError(f"Персонаж с данным классом не может использовать этот предмет. "
                            f"Данный предмет предназначен для: {self.character_class}. "
                            f"Класс персонажа: {character.__class__.__name__}.")
        else:
            result_str = f"Предмет \"{self.name}\" был применен. Персонаж {character.name} получил улучшения! "

            for feature in list(self.features_for_update.keys()):
                character.__setattr__(feature, character.__getattribute__(feature)
                                      + self.features_for_update[feature])

                result_str += f"Характеристика \"{en_ru_features_dict[feature]}\" " \
                              f"была {'увеличена' if self.features_for_update[feature] > 0 else 'уменьшена'} " \
                              f"на {self.features_for_update[feature]}. "
            return result_str

    def info(self):
        """Возвращает строку с информацией о предмете"""

        result = f"Сокровище \"{self.name}\". При использовании изменит следующие характеристики: "

        for name in en_ru_features_dict:
            if self.features_for_update.__contains__(name):
                if self.features_for_update[name] > 0:
                    result += "увеличит"
                else:
                    result += "уменьшит"
                result += f" \"{en_ru_features_dict[name]}\" на {int(self.features_for_update[name])}, "

        return result[:-2] + "."


class HealthPotion(Treasure):
    """Зелье здоровья"""

    name = "Эликсир здоровья"
    character_class = "any"

    features_for_update = {
        "health": 50
    }


class EnergyPotion(Treasure):
    """Зелье энергии"""

    name = "Эликсир энергии"
    character_class = "any"

    features_for_update = {
        "energy": 50
    }


class Staff(Treasure):
    """Посох. Предназначен для класса маг"""

    name = "Посох"
    character_class = "Mage"

    item_names = ["Посох Мерлина", "Посох огня", "Посох грома", "Скипетр Зевса"]

    def __init__(self):
        self.name = get_random_list_element(self.item_names)
        self.features_for_update = {"range": 1, "rca": random.randint(10, 20)}


class Sword(Treasure):
    """Меч. Предназначен для класса воин"""

    name = "Меч"
    character_class = "Warrior"

    item_names = ["Дамоклов меч", "Меч Короля Артура", "Заточенная фальката", "Катана императора"]

    def __init__(self):
        self.name = get_random_list_element(self.item_names)
        self.features_for_update = {"cca": random.randint(10, 30), "energy": random.randint(10, 30),
                                    "health": random.randint(10, 30)}


class Bow(Treasure):
    """Меч. Предназначен для класса лучник"""

    name = "Лук"
    character_class = "Archer"

    item_names = ["Лук Купидона", "Лук ястреба", "Английский длинный лук", "Составной лук"]

    def __init__(self):
        self.name = get_random_list_element(self.item_names)
        self.features_for_update = {"rca": random.randint(10, 30), "energy": random.randint(10, 30)}


class MagicLamp(Treasure):
    """Меч. Предназначен для класса фея"""

    name = "Магическая лампа"
    character_class = "Fairy"

    def __init__(self):
        self.features_for_update = {"rca": random.randint(10, 30), "energy": random.randint(10, 30)}


class TreasureChest(GameItem):
    """Сундук с сокровищами"""

    content_dict = {
        "HealthPotion": HealthPotion,
        "EnergyPotion": EnergyPotion,
        "Staff": Staff,
        "Bow": Bow,
        "Sword": Sword,
        "MagicLamp": MagicLamp,
    }

    def __init__(self, x, y):
        """
        :param x: int, координата x расположения сундука
        :param y: int, координата y расположения сундука
        """
        GameItem.__init__(self, x, y)

    def open(self):
        """Возвращает случайный предмет из списка возможного содержимого сундука"""

        item = self.content_dict[get_random_list_element(list(self.content_dict.keys()))]()
        return item

    def get_tag(self):
        """Возвращает тэг сундука"""
        return self.__class__.__name__.lower()[0]

    def info(self):
        return f"Сундук с сокровищем. Находится в клетке ({self.x}, {self.y})." \
               "\nДля того, чтобы узнать его содержимое, сундук необходимо открыть. "
