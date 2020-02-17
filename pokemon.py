"""
Author: Tushya Iyer, Nolan Crocks
ACIT 2515
Date: 2/17/2020
"""

from typing import List

class Pokemon():

    _MIN_BASE_XP = 80
    _MAX_BASE_XP = 120

    _MIN_LEVEL_UP_XP_MULT = 1.0
    _MAX_LEVEL_UP_XP_MULT = 1.5

    _STARTING_LEVEL = 5
        
    def __init__(self, id: int, species_id: int, source: str, nickname: str = None, item: str = None, ability: str = None) -> None:
	    pass

    
    def _level_up(self) -> None:
        pass


    def _knock_out(self) -> None:
        pass


    @property
    def id(self) -> int:
        pass


    @property
    def pokedex(self) -> List:
        pass


    @property
    def moves(self) -> List:
        pass


    @property
    def xp_till_next_level(self) -> int:
        pass


    @property
    def level(self) -> int:
        pass


    @property
    def ability(self) -> str:
        pass


    @property
    def type(self) -> str:
        pass


    @property
    def attack(self) -> int:
        pass


    @property
    def speed(self) -> int:
        pass


    @property
    def defense(self) -> int:
        pass


    @property
    def total_hp(self) -> int:
        pass


    @property
    def current_hp(self) -> int:
        pass


    @property
    def is_KO(self) -> bool:
        pass


    def use_move(self, move: str) -> None:
        pass


    def add_xp(self, xp_increse: int) -> None:
        pass


    def heal(self, health_increase: int) -> None:
        pass


    def damage(self, health_decrease: int) -> None:
        pass
