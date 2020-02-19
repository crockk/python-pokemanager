"""
Author: Tushya Iyer, Nolan Crocks
ACIT 2515
Date: 2/13/2020
"""

from datetime import date
from random import uniform


class PartyMember:

    _MIN_WEIGHT = 50 #KG
    _MAX_WEIGHT = 1000 #KG

    _MIN_HEIGHT = 80 #CM
    _MAX_HEIGHT = 1500 #CM

    def __init__(self, id: int, species: str, source: str, nickname: str = None, item: str = None) -> None:
        pass


    @property
    def id(self) -> int:
        pass


    @property
    def species(self) -> str:
        pass


    @property
    def name(self) -> str:
        pass


    @name.setter
    def name(self, new_name: str) -> None:
        pass


    @property
    def in_part(self) -> bool:
        pass


    @property
    def weight(self) -> float:
        pass


    @property
    def height(self) -> float:
        pass


    @property
    def description(self) -> str:
        pass


    @property
    def source(self) -> str:
        pass


    @property
    def date_aquired(self) -> date:
        pass


    @property
    def held_item(self) -> str:
        pass


    @held_item.setter
    def held_item(self, item: str) -> None:
        pass

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


