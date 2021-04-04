import random

from . helpers import get_random_list_element, en_ru_features_dict
from . base_classes import GameItem


class Enemy(GameItem):
    """
    Класс враждебных персонажей
    """

    enemies_count = 0

    # Значения характеристик по умолчанию
    default_health = 100
    default_rca = 25
    default_cca = 25

    # Мультипликаторы для разных рас врагов
    # Для каждой расы есть список доступных для нее классов
    enemy_races = {
        "Goblin": {
            "name_ru": "Гоблин",
            "has_class": True,
            "possible_classes": ["Warrior", "Archer"],
            "health_multiplier": 0.5,
            "rca_multiplier": 0.8,
            "cca_multiplier": 0.8
        },

        "Ogre": {
            "name_ru": "Огр",
            "has_class": True,
            "possible_classes": ["Warrior", "Mage"],
            "health_multiplier": 1,
            "rca_multiplier": 0.5,
            "cca_multiplier": 0.5
        },

        "Golem": {
            "name_ru": "Голем",
            "has_class": False,
            "health_multiplier": 3,
            "rca_multiplier": 0.1,
            "cca_multiplier": 0.25
        }

    }

    # Мультипликаторы для главных врагов - боссов
    boss_enemy_races = {
        "Dragon": {
            "name_ru": "Дракон",
            "has_class": False,
            "health_multiplier": 5,
            "rca_multiplier": 1,
            "cca_multiplier": 1
        }
    }

    # Мультипликаторы для разных классов врагов
    enemy_classes = {
        "Warrior": {
            "name_ru": "Воин",
            "health_multiplier": 2,
            "rca_multiplier": 0.5,
            "cca_multiplier": 1
        },
        "Archer": {
            "name_ru": "Лучник",
            "health_multiplier": 1,
            "rca_multiplier": 2,
            "cca_multiplier": 0.25
        },
        "Mage": {
            "name_ru": "Маг",
            "health_multiplier": 1,
            "rca_multiplier": 2,
            "cca_multiplier": 0.1
        }

    }

    def __init__(self, game_engine, difficulty_level, x, y, is_boss=False):
        """
        :param game_engine: GameEngine, объект игрового движка
        :param difficulty_level: int, установленный уровень сложности игры
        :param x: int, координата x расположения врага
        :param y: int, координата y расположения врага
        :param is_boss: bool, True если враг является боссом
        """

        # Устанавливаем расположение объекта
        GameItem.__init__(self, x, y)

        # Генерируем id
        self.id = self.enemies_count + 1

        Enemy.enemies_count += 1

        self.is_boss = is_boss

        self.game_engine = game_engine
        self.protected_spots = []

        # Генерируем коэффициент, на основании котовых будут изменятся изначальные характеристики врагов
        # Характеристика является значением по умолчанию, помноженным на случайный коэффициент,
        # а также мультипликаторы класса и расы врага
        random_coefficients = [random.randint(90, 100) / 100,
                               random.randint(90, 100) / 100,
                               random.randint(90, 100) / 100]

        # У врага три характеристики: здоровье (health), атака в ближнем бою (cca) и атака в дальнем бою (rca)

        if is_boss:
            enemy_race = get_random_list_element(list(self.boss_enemy_races.keys()))
            self.health = int(self.default_health * self.boss_enemy_races[enemy_race]["health_multiplier"] *
                              difficulty_level * random_coefficients[0])
            self.rca = int(self.default_health * self.boss_enemy_races[enemy_race]["rca_multiplier"] *
                           difficulty_level * random_coefficients[1])
            self.cca = int(self.default_health * self.boss_enemy_races[enemy_race]["cca_multiplier"] *
                           difficulty_level * random_coefficients[2])
            self.name = self.boss_enemy_races[enemy_race]["name_ru"]

        else:
            enemy_race = get_random_list_element(list(self.enemy_races.keys()))

            if self.enemy_races[enemy_race]["has_class"]:
                enemy_class = get_random_list_element(list(self.enemy_classes.keys()))
                self.health = int(self.default_health * self.enemy_races[enemy_race]["health_multiplier"] *
                                  self.enemy_classes[enemy_class]["health_multiplier"] *
                                  difficulty_level * random_coefficients[0])
                self.rca = int(self.default_health * self.enemy_races[enemy_race]["rca_multiplier"] *
                               self.enemy_classes[enemy_class]["rca_multiplier"] *
                               difficulty_level * random_coefficients[1])
                self.cca = int(self.default_health * self.enemy_races[enemy_race]["cca_multiplier"] *
                               self.enemy_classes[enemy_class]["cca_multiplier"] *
                               difficulty_level * random_coefficients[2])
                self.name = self.enemy_races[enemy_race]["name_ru"] + " " + self.enemy_classes[enemy_class]["name_ru"]

            # Если у расы врага не может быть класса
            else:
                self.health = int(self.default_health * self.enemy_races[enemy_race]["health_multiplier"] *
                                  difficulty_level * random_coefficients[0])
                self.rca = int(self.default_health * self.enemy_races[enemy_race]["rca_multiplier"] *
                               difficulty_level * random_coefficients[1])
                self.cca = int(self.default_health * self.enemy_races[enemy_race]["cca_multiplier"] *
                               difficulty_level * random_coefficients[2])
                self.name = self.enemy_races[enemy_race]["name_ru"]

    def get_tag(self):
        """Возвращает тэг объекта"""
        if self.is_boss:
            return "b"

        return self.__class__.__name__[0].lower() + str(self.id)

    def get_id(self):
        """Возвращает id объекта"""
        return self.id

    def get_rca(self):
        """Возвращает атаку в дальнем бою объекта"""
        return self.rca

    def get_cca(self):
        """Возвращает атаку в ближнем бою объекта"""
        return self.cca

    def get_current_health(self):
        """Возвращает текущее здоровье объекта"""
        return self.health

    def _die(self):
        """Метод для умерщвления объекта и очистки данных, где он присутствует"""
        self.game_engine.game_field[self.y - 1][self.x - 1].set_spot_owner(None)
        for spot in self.protected_spots:
            spot.loose_spot_protection(self.id)

        self.game_engine.field_tags.remove(self.get_tag())
        del self.game_engine.items_dict[self.get_tag()]

        if self.get_tag() == "b":
            self.game_engine.add_score(self.game_engine.scores["boss"])
        else:
            self.game_engine.add_score(self.game_engine.scores["enemy"])

    def decrease_health(self, value):
        """Метод для осуществления механики нанесения урона врагу"""
        self.health = self.health - value

        response = str()

        if self.health <= 0:
            self._die()
            response += f"Враг \"{self.name}\" получил {value} урона. \"{self.name}\" был повержен."
        else:
            response += f"Враг \"{self.name}\" получил {value} урона. Осталось здоровья: {self.health}."

        return response

    def set_protected_spots(self, spots):
        """Устанавливает список ячеек, которые защищаются данным врагом"""
        self.protected_spots = spots

    def add_protected_spot(self, spot):
        """Добавляет ячейку в список ячеек, которые защищаются данным врагом"""
        self.protected_spots.append(spot)

    def get_protected_spots(self):
        """Возвращает список ячеек, которые защищаются данным врагом"""
        return self.protected_spots

    def info(self):
        result = f"Враг N{self.id}. Имя: \"{self.name}\". Характеристики: "

        for name in en_ru_features_dict:
            if hasattr(self, name):
                result += f"{en_ru_features_dict[name]} {int(self.__getattribute__(name))}, "

        result = result[:-2] + ". "
        result += f"Находится в точке ({self.x}, {self.y})."

        return result
