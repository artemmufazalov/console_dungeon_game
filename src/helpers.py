import random
import functools


en_ru_features_dict = {
    "health": "здоровье",
    "energy": "энергия",
    "range": "радиус атаки",
    "cca": "атака в ближнем бою",
    "rca": "атака в дальнем бою",
    "aec": "расход энергии при атаке",
    "mec": "расход энергии при движении"
}
"""Словарь с русскоязычными названиями характеристик"""

class_ru_names = {
    "mage": "Маг",
    "warrior": "Воин",
    "archer": "Лучник",
    "fairy": "Фея"
}
"""Словарь с русскоязычными названиями классов"""


def get_random_list_element(values_list):
    """Функция для получения случайного элемента из списка"""
    if len(values_list) == 1:
        return values_list[0]

    return values_list[random.randint(0, len(values_list) - 1)]


def __track_class_calls__(class_declaration):
    """
    Функция - декоратор для классов.
    Устанавливает декораторы для всех методов класса,
    благодаря которым в консоль выводится информация о вызванном методе и объекте.
    Не работает для методов классов наследников, если они не определены в изначальном классе.
    Необходима для тестирования процессов взаимодействия с классом извне.
    """
    def notify(func):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            class_name = self.name if hasattr(self, "name") else self.__class__.__name__
            print(f"--- {class_name}: был вызван метод {func.__name__}{args, kwargs}.")
            return func(self, *args, **kwargs)
        return wrapper

    for name in class_declaration.__dict__:
        method = getattr(class_declaration, name)
        if hasattr(method, "__call__"):
            setattr(class_declaration, name, notify(method))

    return class_declaration
