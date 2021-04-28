from .enemy_characters import Enemy
from .game_spot import GameSpot
from .playable_characters import Warrior, Mage, Archer, Fairy
from .inventory import Inventory
from .items import HealthPotion, EnergyPotion, TreasureChest
from .helpers import get_random_list_element


class GameEngine:
    """
    Класс игрового движка. Хранит данные текущей игры
    """

    # Размеры игрового поля
    _game_field_width = 8
    _game_field_length = 8

    # Данные запущенной игры
    difficulty = 1
    is_game_on = False
    game_field = []
    field_tags = []
    friendly_tags = []
    items_dict = {}
    inventory = None
    player_actions = []

    # Количество очков за игровые действия
    scores = {
        "chest": 50,
        "enemy": 100,
        "boss": 200,
        "friendly_character_death": -100,
        "action": 5
    }

    # Начальные позиции дружественных персонажей
    _characters_default_positions = {
        "fairy": [1, 1],
        "archer": [1, 2],
        "mage": [2, 1],
        "warrior": [2, 2]
    }

    # Классы дружественных игровых персонажей
    _friendly_classes = {
        "fairy": Fairy,
        "archer": Archer,
        "mage": Mage,
        "warrior": Warrior
    }

    # Начальные позиции врагов и ячейки, которые они защищают
    _enemies_positions = [
        {"position": [2, 5],
         "protected": [[1, 5], [1, 6], [1, 7], [1, 8], [2, 6], [2, 7], [2, 8], [3, 5]]},
        {"position": [3, 6],
         "protected": [[3, 7], [3, 8], [4, 6], [4, 7], [4, 8], [5, 6], [5, 8]]},
        {"position": [5, 2],
         "protected": [[5, 1], [5, 3], [6, 1], [6, 2], [7, 1], [7, 2], [8, 1], [8, 2]]},
        {"position": [6, 3],
         "protected": [[6, 4], [7, 3], [7, 4], [7, 5], [8, 3], [8, 4], [8, 5]]},
        {"position": [5, 5],
         "protected": [[5, 6], [5, 7], [6, 5], [7, 5], [6, 6]]},
        {"position": [6, 7],
         "protected": [[6, 8], [7, 7], [7, 8]]},
        {"position": [7, 6],
         "protected": [[7, 7], [8, 6], [8, 7]]},
    ]

    # Координаты босса
    _main_enemy_default_position = [8, 8]

    # Координаты сундуков с сокровищами
    _treasures_variable_positions = [
        [[1, 7], [2, 7]],
        [[3, 8], [4, 8]],
        [[7, 1], [7, 2]],
        [[8, 3], [8, 4]]
    ]

    def __init__(self, game, game_id, logger):

        self.game = game
        self.game_id = game_id
        self.logger = logger
        self.score = 0
        self.is_game_on = True
        self.game_field = []
        self._init_result_output = []

    def _init_empty_game_field(self):
        """Функция создания пустого игрового поля"""

        for x in range(self._game_field_length):
            self.game_field.append([])
            for y in range(self._game_field_width):
                # Здесь транспонируются координаты. В дальнейшем обращение к игровому полю будет формата [y][x]
                game_spot = GameSpot(y + 1, x + 1, False, None, False, [])
                self.game_field[x].append(game_spot)

    def _append_init_results_output(self, line):
        self._init_result_output.append(line)

    def get_current_field_raw(self):
        raw_view = []

        for i in range(len(self.game_field)):
            line = self.game_field[self._game_field_width - i - 1]

            def get_tag(a):
                return a.request_occupation_tag()

            raw_view.append(list(map(get_tag, line)))

        return raw_view

    def get_current_field_view(self):
        """Функция для отображения игрового поля"""

        result_as_lines = []

        for i in range(len(self.game_field)):
            line = self.game_field[self._game_field_width - i - 1]

            def get_tag(a):
                return a.request_occupation_tag() if len(a.request_occupation_tag()) == 2 \
                    else f' {a.request_occupation_tag()}'

            result_as_lines.append(f"{self._game_field_width - i}| " + f"{' '.join(list(map(get_tag, line)))}")

            i += 1

        vert_lines_count = []

        for x in range(self._game_field_width):
            vert_lines_count.append(str(x + 1))

        result_as_lines.append("  " + "---" * self._game_field_width)
        result_as_lines.append("    " + "  ".join(vert_lines_count))

        return "\n".join(result_as_lines)

    def get_tags(self):
        """Возвращает список тэгов, присутствующих на игровом поле (кроме сундуков с сокровищами)"""
        return self.field_tags

    def get_friendly_tags(self):
        """Возвращает список тэгов дружественных персонажей, присутствующих на игровом поле"""
        return self.friendly_tags

    def get_width(self):
        """Возвращает ширину игрового поля"""
        return self._game_field_width

    def get_length(self):
        """Возвращает длину игрового поля"""
        return self._game_field_length

    def start_game(self):
        """Начало игры. Инициализирует игровое поле и игровые объекты"""

        self._init_result_output = []

        self._init_empty_game_field()
        self._init_inventory()
        self._init_treasures()
        self._init_characters()
        self._init_enemies()

        self._append_init_results_output(f"\n{self.help()}")

        return "\n".join(self._init_result_output)

    def _init_inventory(self):
        """Создает рюкзак и добавляет в него начальный запас эликсиров"""

        self._append_init_results_output("\n...Инициализация рюкзака...")
        self.inventory = Inventory()
        self._append_init_results_output("Создан рюкзак.")
        self._append_init_results_output("В рюкзак добавлены предметы:")
        health_potion = HealthPotion()
        self.inventory.add_item(health_potion)
        self._append_init_results_output(f"* {health_potion.info()}")
        energy_potion = EnergyPotion()
        self.inventory.add_item(energy_potion)
        self._append_init_results_output(f"* {energy_potion.info()}")

    def _init_treasures(self):
        """Инициализирует на игровом поле сундуки с сокровищами"""

        self._append_init_results_output("\n...Инициализация сундуков с сокровищами...")

        for coords in self._treasures_variable_positions:
            chest_coords = get_random_list_element(coords)
            treasure_chest = TreasureChest(chest_coords[0], chest_coords[1])
            self.game_field[chest_coords[0] - 1][chest_coords[1] - 1].set_spot_owner(treasure_chest)
            self._append_init_results_output(f"В клетку ({chest_coords[1]}, {chest_coords[0]}) был добавлен сундук с сокровищем.")

    def _init_characters(self):
        """Инициализирует на игровом поле дружественных персонажей"""

        self._append_init_results_output("\n...Инициализация игровых персонажей...")

        for key in list(self._characters_default_positions.keys()):
            coords = self._characters_default_positions[key]
            character = self._friendly_classes[key](coords[1], coords[0], self)
            self.game_field[coords[0] - 1][coords[1] - 1].set_spot_owner(character)
            self.friendly_tags.append(character.get_tag())
            self.field_tags.append(character.get_tag())
            self.items_dict[character.get_tag()] = character
            self._append_init_results_output(f"Создан игровой персонаж. {character.info()}")

    def _init_enemies(self):
        """Инициализирует на игровом поле враждебных персонажей"""

        self._append_init_results_output("\n...Инициализация врагов...")

        for enemy_positions in self._enemies_positions:
            coords = enemy_positions["position"]
            enemy = Enemy(self, 1, coords[0], coords[1], False)
            self.game_field[coords[1] - 1][coords[0] - 1].set_spot_owner(enemy)
            self.field_tags.append(enemy.get_tag())
            self.items_dict[enemy.get_tag()] = enemy
            protected_coords = enemy_positions["protected"]
            for protected in protected_coords:
                spot = self.game_field[protected[1] - 1][protected[0] - 1]
                spot.set_spot_protector(enemy)
                enemy.add_protected_spot(spot)

            self._append_init_results_output(f"* {enemy.info()}")

        boss = Enemy(self,
                     self.difficulty,
                     self._main_enemy_default_position[0],
                     self._main_enemy_default_position[1],
                     True)
        self.game_field[self._main_enemy_default_position[1] - 1][self._main_enemy_default_position[0] - 1] \
            .set_spot_owner(boss)
        self.field_tags.append(boss.get_tag())
        self.items_dict[boss.get_tag()] = boss
        self._append_init_results_output(f"* {boss.info()}\n")

    def add_player_action(self, subject, action, args):
        """
        Добавляет действие пользователя в историю\n
        :param subject: PlayableCharacter, персонаж, который выполняет действие
        :param action: str, действие персонажа
        :param args: list [], список аргументов действия
        """
        self.player_actions.append({"subject": subject, "action": action, "args": args})

    def get_player_actions(self):
        """Возвращает список действия персонажей игрока """
        return self.player_actions

    def add_score(self, score):
        """
        Увеличивает счет на переданное значение\n
        :param score: int, величина, на которую увеличивается счет
        """
        self.score += score

    def decrease_score(self, score):
        """
        Уменьшает счет на переданное значение\n
        :param score: int, величина, на которую уменьшается счет
        """
        self.score -= score

    def _calculate_final_score(self):
        """Рассчитывает и возвращает итоговый игровой счет"""
        actions_score = len(self.player_actions) * self.scores["action"]
        self.score -= actions_score
        return self.score

    def end_game(self, status=""):
        """Функция для завершения игры"""
        self.is_game_on = False

        score = self._calculate_final_score()
        game_status = "победой" if status == "success" else "поражением" if status == "failure" else "досрочно"

        self.logger.log(game_id=self.game_id,
                        game_event="Окончание игры",
                        message=f"Игра окончена {game_status}. "
                                + f"Было отдано {len(self.get_player_actions())} игровых команд. "
                                + f"Игровой счет: {score}.")

        self.game.set_off()

        return f"Игра окончена. Ваш счет: {score}."

    def end_game_success(self):
        """Функция для завершения игры, если все враги повержены"""
        result = "\nГлавный враг повержен! Вы победили!\n"
        result += self.end_game("success")

        return result

    def end_game_failure(self):
        """Функция для завершения игры, если все дружественные персонажи погибли и игра не может быть продолжена"""
        result = "\nВсе ваши персонажи погибли! Враги победили!\n"
        result += self.end_game("failure")

        return result

    def check_is_game_on(self):
        """Проверяет, выполняются ли какие-либо из условий завершения игры"""
        if len(self.friendly_tags) == 0:
            return self.end_game_failure()
        elif "b" not in self.field_tags and "b" not in list(self.items_dict.keys()):
            return self.end_game_success()

        return ''

    @staticmethod
    def help():
        """Возвращает инструкцию по игре"""
        with open("src/help.txt", encoding='utf-8', errors='ignore') as file:
            text = file.read()
            return text
