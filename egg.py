"""
Author: Tushya Iyer, Nolan Crocks
ACIT 2515
Date: 2/17/2020
"""

from party_member import PartyMember
from typing import List
from random import randint


class Egg(PartyMember):

    _MEMBER_TYPE = "Egg"

    _MIN_STEPS = 1000  # steps
    _MAX_STEPS = 5000  # steps

    def __init__(self, id: int, pokedex_dum: int, source: str, nickname: str = None, item: str = None):
        super().__init__(id, pokedex_dum, source, nickname, item)

        self._steps_required = self._rand_steps()

        # This value is decremented by the walk method until it hatches
        self._steps_remaining = self._steps_required

        self._hatched = False
        pass

    @property
    def steps_required(self) -> int:
        return self._steps_required

    @property
    def steps_remaining(self) -> int:
        return self._steps_remaining

    def walk(self, steps: int) -> None:
        self._steps_remaining -= steps
        if self._steps_remaining <= 0:
            self._hatched = True

    @classmethod
    def _rand_steps(cls) -> int:
        return randint(cls._MIN_STEPS, cls._MAX_STEPS)

    @classmethod
    def member_type(cls):
        return cls._MEMBER_TYPE
