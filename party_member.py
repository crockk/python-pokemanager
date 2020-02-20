"""
Author: Tushya Iyer, Nolan Crooks
ACIT 2515
Date: 2/13/2020
"""
from abc import abstractmethod, ABC
from datetime import date, datetime
from random import uniform


class PartyMember(ABC):
    _MIN_WEIGHT = 50  # KG
    _MAX_WEIGHT = 1000  # KG

    _MIN_HEIGHT = 80  # CM
    _MAX_HEIGHT = 1500  # CM

    def __init__(self, id: int, pokedex_num: int, source: str, nickname: str = None, item: str = None) -> None:

        self._validate_int(id, 1, "ID must be an Integer greater than or equal to 1")

        self._validate_int(pokedex_num, 1, "Pokedex Number must be greater than or equal to 1")

        self._validate_string(source, "Source must be a none-blank String")

        if nickname:
            self._validate_string(nickname, "Nickname must be a none-blank String")

        if item:
            self._validate_string(item, "Item must be a none-blank String")

        self._id = id
        self._pokedex_num = pokedex_num
        self._source = source
        self._nickname = nickname
        self._item = item

        self._in_party = False
        self._weight = self._rand_weight()
        self._height = self._rand_height()
        self._date_aquired = datetime.now().date()

    @property
    def id(self) -> int:
        return self._id

    @property
    def pokedex_num(self) -> str:
        return self._pokedex_num

    @property
    def name(self) -> str:
        return self._nickname

    @name.setter
    def name(self, new_name: str) -> None:
        self._validate_string(new_name, "Nickname must be a none-blank String")

        self._nickname = new_name

    @property
    def in_party(self) -> bool:
        return self._in_party

    @property
    def weight(self) -> float:
        return self._weight

    @property
    def height(self) -> float:
        return self._height

    @abstractmethod
    def description(self) -> str:
        raise NotImplementedError

    @property
    def source(self) -> str:
        return self._source

    @property
    def date_aquired(self) -> date:
        return self._date_aquired

    @property
    def held_item(self) -> str:
        if self._item:
            return self._item
        else:
            return "None"

    @held_item.setter
    def held_item(self, item: str) -> None:
        self._validate_string(item, "Item must be a none-blank String")

        self._item = item

    @classmethod
    def _rand_weight(cls) -> float:
        return round(uniform(cls._MIN_WEIGHT, cls._MAX_WEIGHT), 2)

    @classmethod
    def _rand_height(cls) -> float:
        return round(uniform(cls._MIN_HEIGHT, cls._MAX_HEIGHT), 2)

    @staticmethod
    def _validate_int(num: int, min_val: int, error_msg: str) -> None:
        """Private method. Used to validate integers according to a minimum value and type. Raises an error with a custom error message"""
        if type(num) is not int:
            raise TypeError(error_msg + f"\nNot type {type(num)}")
        if num < min_val:
            raise ValueError(error_msg)

    @staticmethod
    def _validate_string(string: str, error_msg: str) -> None:
        """Private method. Used to validate strings according to type. Raises an error with a custom error message"""
        if type(string) is not str:
            raise TypeError(error_msg + f"\nNot type {type(string)}")
        if not string:
            raise ValueError(error_msg)

    @abstractmethod
    def member_type(self):
        raise NotImplementedError
