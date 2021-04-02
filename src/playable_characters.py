from . base_classes import GameItem, Flyable, Movable
from . errors import GameError
from . helpers import class_ru_names, __track_class_calls__, en_ru_features_dict


# @__track_class_calls__
class PlayableCharacter(GameItem, Movable):
    """Класс игровых персонажей"""

    # Значения характеристик по умолчанию
    default_health = 200
    default_energy = 100
    default_close_attack = 70
    default_ranged_attack = 50
    default_rca_range = 1
    default_attack_energy_cost = 5
    default_movement_energy_cost = 1

    name = "Персонаж"

    def __init__(self, health_multiplier, energy_multiplier,
                 cca_multiplier, rca_multiplier,
                 rca_range_multiplier, attack_energy_cost_multiplier,
                 movement_energy_cost_multiplier, game_engine, x=0, y=0):

        GameItem.__init__(self, x, y)

        self.game_engine = game_engine

        # Получаем значения характеристик как произведение значений по умолчанию и мультипликаторов класса
        # Русский перевод характеристик находится в helpers в en_ru_features_dict
        self.health = int(PlayableCharacter.default_health * health_multiplier)
        self.energy = int(PlayableCharacter.default_energy * energy_multiplier)
        self.range = int(PlayableCharacter.default_rca_range * cca_multiplier)
        self.cca = int(PlayableCharacter.default_close_attack * rca_multiplier)
        self.rca = int(PlayableCharacter.default_ranged_attack * rca_range_multiplier)
        self.aec = int(PlayableCharacter.default_attack_energy_cost * attack_energy_cost_multiplier)
        self.mec = int(PlayableCharacter.default_movement_energy_cost * movement_energy_cost_multiplier)

        self.name = class_ru_names[self.__class__.__name__.lower()]

    def init_multipliers(self):
        """Возвращает список с мультипликаторами характеристик для классов"""
        return [self.default_health_multiplier,
                self.default_energy_multiplier,
                self.default_rca_range_multiplier,
                self.default_cca_multiplier,
                self.default_rca_multiplier,
                self.default_attack_energy_cost_multiplier,
                self.default_movement_energy_cost_multiplier]

    def get_tag(self):
        """Возвращает тэг персонажа"""
        return self.__class__.__name__[0].lower()

    def info(self):
        result = f"Ваш персонаж, класс \"{class_ru_names[self.__class__.__name__.lower()]}\". Характеристики: "
        for value in en_ru_features_dict:
            result += f"\"{en_ru_features_dict[value]}\" {self.__getattribute__(value)}, "

        result = result[:-2] + "."
        result += f"Находится в точке ({self.x}, {self.y})."

        return result

    def _die(self):
        """Отвечает за смерть персонажа и очистку данных, связанных с ним"""
        self.game_engine.game_field[self.y - 1][self.x - 1].set_spot_owner(None)
        self.game_engine.add_score(self.game_engine.scores["friendly_character_death"])

        self.game_engine.field_tags.remove(self.get_tag())
        self.game_engine.friendly_tags.remove(self.get_tag())
        del self.game_engine.items_dict[self.get_tag()]

        return f"Ваш персонаж \"{self.name}\" погиб!"

    def check_is_enemy(self, enemy):
        """Проверяет, является ли переданный объект врагом"""

        if not enemy:
            raise GameError("В выбранной ячейке нет врага!")
        elif enemy.__class__.__name__.lower()[0] in self.game_engine.friendly_tags:
            raise GameError("Вы не можете атаковать дружественного персонажа!")
        elif enemy.__class__.__name__.lower() != "enemy":
            raise GameError("Вы не можете атаковать объекты, не являющиеся врагами!")

    def check_is_valid_tag(self, tag):
        """Проверяет, является ли переданный тэг корректным"""

        if tag not in list(self.game_engine.items_dict.keys()):
            raise GameError("Введен некорректный тэг!")

    def attack(self, enemy):
        """Отвечает за ближний бой персонажа с врагом"""

        self.check_is_enemy(enemy)

        distance = max(abs(enemy.x - self.x), abs(enemy.y - self.y))
        if distance > 1:
            raise GameError("Враг находится слишком далеко!")
        else:
            result = f"Бой между \"{self.name}\" и \"{enemy.name}\" начался!"
            result += f"\n{enemy.decrease_health(self.cca)}"

            damage = enemy.get_cca()
            self.health -= damage
            result += f"\n\"{enemy.name}\" атакует!"
            result += f"\nПерсонаж \"{self.name}\" получил {damage} урона! Осталось здоровья: {self.health}."
            if self.health <= 0:
                result += f"\n{self._die()}"

            return result

    def shoot(self, enemy):
        """Отвечает бой персонажа с врагом на расстоянии"""

        self.check_is_enemy(enemy)

        distance = max(abs(enemy.x - self.x), abs(enemy.y - self.y))
        if distance > self.range:
            raise GameError("Враг находится слишком далеко!")
        else:
            result = f"Бой между \"{self.name}\" и \"{enemy.name}\" начался!"
            result += f"\n\"{self.name}\" стреляет во врага!"
            result += f"\n{enemy.decrease_health(self.rca)}"

            damage = enemy.get_rca()
            self.health -= damage
            result += f"\n\"{enemy.name}\" атакует!"
            result += f"\nПерсонаж \"{self.name}\" получил {damage} урона! Осталось здоровья: {self.health}."
            if self.health <= 0:
                result += f"\n{self._die()}"

            return result

    def attack_by_tag(self, enemy_tag):
        """
        Ближний бой с врагом по переданному тэгу\n
        :param enemy_tag: str, тэг врага
        """

        self.check_is_valid_tag(enemy_tag)

        target = self.game_engine.items_dict[enemy_tag]
        return self.attack(target)

    def attack_by_coords(self, x, y):
        """
        Ближний бой с врагом по переданным координатам\n
        :param x: int, координата x расположения врага
        :param y: int, координата y расположения врага
        """

        target = self.game_engine.game_field[y - 1][x - 1].get_spot_owner()
        return self.attack(target)

    def shoot_by_tag(self, enemy_tag):
        """
        Дальний бой с врагом по переданному тэгу\n
        :param enemy_tag: str, тэг врага
        """

        self.check_is_valid_tag(enemy_tag)

        target = self.game_engine.items_dict[enemy_tag]
        return self.shoot(target)

    def shoot_by_coords(self, x, y):
        """
        Дальний бой с врагом по переданным координатам\n
        :param x: int, координата x расположения врага
        :param y: int, координата y расположения врага
        """

        target = self.game_engine.game_field[y - 1][x - 1].get_spot_owner()
        return self.shoot(target)

    def use(self, potion_name):
        """
        Использование эликсира из рюкзака\n
        :param potion_name: str, "health" для эликсиров здоровья, "energy" для эликсиров энергии
        """

        potion = self.game_engine.inventory.get_potion(potion_name)
        result = potion.use(self)

        if result:
            self.game_engine.inventory.del_item(potion)

        return result

    def perform_action(self, action, args):
        """
        Выполнение персонажем переданного действия\n
        :param action: str, действие персонажа
        :param args: list [], список аргументов функции действия
        """

        result = str()

        if action == "attack":
            if len(args) == 2:
                result = self.attack_by_coords(int(args[0]), int(args[1]))

            elif len(args) == 1:
                result =  self.attack_by_tag(args[0])

            else:
                raise GameError("Неверное число аргументов.")

        elif action == "shoot":
            if type(self) == Warrior:
                raise GameError("Воин не умеет атаковать издалека. Попробуйте использовать атаку в ближнем бою.")

            if len(args) == 2:
                result = self.shoot_by_coords(int(args[0]), int(args[1]))
            elif len(args) == 1:
                result = self.shoot_by_tag(args[0])
            else:
                raise GameError("Неверное число аргументов.")

        elif action == "move":
            if len(args) == 2:
                result = self.move(int(args[0]), int(args[1]))
            else:
                raise GameError("Неверное число аргументов.")

        elif action == "fly":
            if type(self) != Fairy:
                raise GameError("Только феи умеют летать!")
            else:
                result = self.fly(int(args[0]), int(args[1]))

        elif action == "use":
            result = self.use(args[0])

        else:
            raise GameError("Передано неверное описание действия.")

        if result:
            self.game_engine.add_player_action("action", args)

        return result


class Warrior(PlayableCharacter):
    """Воин"""

    default_health_multiplier = 1
    default_energy_multiplier = 0.5
    default_cca_multiplier = 1
    default_rca_multiplier = 0
    default_rca_range_multiplier = 1
    default_attack_energy_cost_multiplier = 1
    default_movement_energy_cost_multiplier = 1

    def __init__(self, x, y, game_engine):
        PlayableCharacter.__init__(self, *self.init_multipliers(), game_engine, x=x, y=y)


class Archer(PlayableCharacter):
    """Лучник"""

    default_health_multiplier = 0.5
    default_energy_multiplier = 0.5
    default_cca_multiplier = 0.5
    default_rca_multiplier = 2
    default_rca_range_multiplier = 3
    default_attack_energy_cost_multiplier = 1
    default_movement_energy_cost_multiplier = 1

    def __init__(self, x, y, game_engine):
        PlayableCharacter.__init__(self, *self.init_multipliers(), game_engine, x=x, y=y)


class Mage(PlayableCharacter):
    """Маг"""

    default_health_multiplier = 0.5
    default_energy_multiplier = 2
    default_cca_multiplier = 0.2
    default_rca_multiplier = 2
    default_rca_range_multiplier = 2
    default_attack_energy_cost_multiplier = 1
    default_movement_energy_cost_multiplier = 1

    def __init__(self, x, y, game_engine):
        PlayableCharacter.__init__(self, *self.init_multipliers(), game_engine, x=x, y=y)


class Fairy(PlayableCharacter, Flyable):
    """Фея"""

    default_health_multiplier = 0.2
    default_energy_multiplier = 1
    default_cca_multiplier = 0
    default_rca_multiplier = 1
    default_rca_range_multiplier = 2
    default_attack_energy_cost_multiplier = 1
    default_movement_energy_cost_multiplier = 0.5

    def __init__(self, x, y, game_engine):
        PlayableCharacter.__init__(self, *self.init_multipliers(), game_engine, x=x, y=y)
