"""
Author: Tushya Iyer, Nolan Crooks
ACIT 2515
Date: 2/17/2020
"""

from peewee import CharField, IntegerField, DecimalField, DateField, BooleanField, ForeignKeyField
from party_member import PartyMember
from party_manager import PartyManager
from typing import List, Dict
from random import randint
from pokedex import RandomStats


class Egg(PartyMember):
    """ Defines the subclass Egg which is a child of PartyMember

    This class is relatively simple, only adding a few new properties to the abstract
    class PartyMember it inherits from.

    _steps_required is the number of steps that are required to hatch the egg.
    _steps_remaining is the number of steps that are remaining to hatch the egg.
    _hatched is a boolean value which tells PartyManager whether or not to hatch the egg (turn it into a pokemon).

    CLASS VARIABLES:
    _MEMBER_TYPE: The type of party member. In this case, it is "Egg"

    _MIN_STEPS, _MAX_STEPS: Defines the range in which the _steps_required is generated between.

    """

    # _MEMBER_TYPE = "Egg"

    hatched = BooleanField(default=False)
    steps_required = IntegerField(column_name="steps_required", default=RandomStats.rand_steps())
    steps_remaining = IntegerField(column_name="steps_remaining", default=0)
    player = ForeignKeyField(PartyManager, backref='eggs')


    # def add_steps(self, steps: int) -> None:
    #     """ Decrements _steps_remaining by param steps. If _steps_remaining <= 0, _hatched property is set to True.

    #     :param int steps: Number of steps to decrement _steps_remaining by.
    #     :return: No return
    #     :rtype: None

    #     """
    #     self._steps_remaining -= steps
    #     if self._steps_remaining <= 0:
    #         self._hatched = True

    # @property
    # def description(self) -> str:
    #     """ Returns a description of the Egg """
    #     return f"Your {self._nickname} is {self._height}cm tall and {self._weight}kg. " \
    #            f"{ 'Currently in party.' if self._in_party else 'Not currently in party'}"

    # def to_dict(self) -> dict:
    #     """ Converts current instance attributes into dictionary format and returns it

    #     :return: Dictionary of all instance attributes
    #     :rtype: dict

    #     """
    #     dik = {
    #         "id": self._id,
    #         "member_type": self.member_type(),
    #         "pokedex_num": self._pokedex_num,
    #         "source": self._source,
    #         "nickname":  self._nickname,
    #         "item": self._item,

    #         "in_party": self._in_party,
    #         "weight": self._weight,
    #         "height": self._height,
    #         "date_acquired": str(self._date_acquired),

    #         "steps_required": self._steps_required,
    #         "steps_remaining": self._steps_remaining,
    #         "hatched": self._hatched
    #     }
    #     return dik
