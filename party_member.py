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
    def rand_weight(cls) -> float:
        return round(uniform(cls._MIN_WEIGHT, cls._MAX_WEIGHT), 2)

    @classmethod
    def rand_height(cls) -> float:
        return round(uniform(cls._MIN_HEIGHT, cls._MAX_HEIGHT), 2)

    # ^ can't we just use one function for these v
    @classmethod
    def rand_float(cls, min, max) -> float:
        return round(uniform(min, max), 2)


