"""
Author: Tushya Iyer, Nolan Crocks
ACIT 2515
Date: 2/17/2020
"""
from party_member import PartyMember
from typing import List
from random import randint, uniform
from math import ceil


class Pokemon(PartyMember):
    _MIN_BASE_XP = 80
    _MAX_BASE_XP = 120

    _MIN_LEVEL_UP_XP_MULT = 1.0
    _MAX_LEVEL_UP_XP_MULT = 1.5

    _STARTING_LEVEL = 5

    _MIN_BATTLE_STAT = 3
    _MAX_BATTLE_STAT = 18

    _MIN_BASE_HP = 15
    _MAX_BASE_HP = 35

    def __init__(self, id: int, species: str, source: str, nickname: str = None, item: str = None,
                 ability: str = None) -> None:

        super().__init__(id, species, source, nickname, item)

        super()._validate_string(ability, "Ability must be a none-blank String")

        self._ability = ability

        self._next_level_xp = self._rand_base_xp()
        self._current_level_xp = 0
        self._level = self._STARTING_LEVEL

        self._attack = self._rand_battle_stat()
        self._defense = self._rand_battle_stat()
        self._speed = self._rand_battle_stat()

        self._total_hp = self._rand_base_hp()
        self._current_hp = self._total_hp

        self._is_KO = False

    @property
    def id(self) -> int:
        return self._id

    @property
    def pokedex(self) -> List:
        pass

    @property
    def moves(self) -> List:
        pass

    @property
    def xp_till_next_level(self) -> int:
        return self._next_level_xp - self._current_level_xp

    @property
    def level(self) -> int:
        return self._level

    @property
    def ability(self) -> str:
        if self._ability:
            return self._ability
        else:
            return "None"

    @property
    def type(self) -> str:
        pass

    @property
    def attack(self) -> int:
        return self._attack

    @property
    def speed(self) -> int:
        return self._speed

    @property
    def defense(self) -> int:
        return self._defense

    @property
    def total_hp(self) -> int:
        return self._total_hp

    @property
    def current_hp(self) -> int:
        return self._current_hp

    @property
    def is_KO(self) -> bool:
        return self._is_KO

    def use_move(self, move: str) -> None:
        pass

    def add_xp(self, xp_increse: int) -> None:
        super()._validate_int(xp_increse, 0, "XP increase must be an Integer greater than or equal to 0")

        if xp_increse + self._current_level_xp >= self._next_level_xp:
            xp_added = self._next_level_xp - self._current_level_xp
            self._level_up()
            # are we allowed recursion???
            self.add_xp(xp_increse - xp_added)
        else:
            self._current_level_xp += xp_increse

    def heal(self, health_increase: int) -> None:
        super()._validate_int(health_increase, 1, "Health increase must be an Integer greater than or equal to 1")

        if health_increase + self._current_hp >= self._total_hp:
            self._current_hp = self._total_hp
        else:
            self._current_hp += health_increase

    def damage(self, health_decrease: int) -> None:
        super()._validate_int(health_decrease, 1, "Damage must be an Integer greater than or equal to 1")

        if self._current_hp - health_decrease <= 0:
            self._knock_out()
        else:
            self._current_hp -= health_decrease

    def _level_up(self) -> None:

        self._level += 1
        self._current_level_xp = 0
        self._next_level_xp = ceil(self._next_level_xp * self._rand_xp_level_up_multiplier())

        print(f"{self.name} has leveled up to level {self.level}!!")

    def _knock_out(self) -> None:
        self._is_KO = True
        print(f"{self.name} was knocked out")

    @classmethod
    def _rand_base_xp(cls) -> int:
        return randint(cls._MIN_BASE_XP, cls._MAX_BASE_XP)

    @classmethod
    def _rand_xp_level_up_multiplier(cls) -> float:
        return round(uniform(cls._MIN_LEVEL_UP_XP_MULT, cls._MAX_LEVEL_UP_XP_MULT), 2)

    @classmethod
    def _rand_battle_stat(cls) -> int:
        return randint(cls._MIN_BATTLE_STAT, cls._MAX_BATTLE_STAT)

    @classmethod
    def _rand_base_hp(cls) -> int:
        return randint(cls._MIN_BASE_HP, cls._MAX_BASE_HP)
