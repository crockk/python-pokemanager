"""
Author: Tushya Iyer, Nolan Crooks
ACIT 2515
Date: 2/17/2020
"""

from party_member import PartyMember
from typing import List, Dict
from random import randint


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

    _MEMBER_TYPE = "Egg"

    _MIN_STEPS = 1000  # steps
    _MAX_STEPS = 5000  # steps

    def __init__(self, id: int, pokedex_num: int, source: str, nickname: str = None, item: str = None, json: Dict = None):
        """ Initializes the instance properties

        In addition to the superclass init, this function adds _steps_required, _steps_remaining, and _hatched as
        properties for the class. These properties are defined in the help for the class Egg.

        :param int id: Automatically assigned id (incremented each time a new Pokemon or egg is created)
        :param int pokedex_num: The Pokedex number of the Pokemon within the egg, corresponding to a species.
        :param str source: The location where the egg was aquired.
        :param str nickname: The Pokemon's given name (set once the egg hatches, so set to None for now).
        :param str item: The item held by the Pokemon, if any (set once the egg hatches, so set to None for now).
        :return: No return
        :rtype: None

        """
        super().__init__(id, pokedex_num, source, nickname, item, json)
        if json is not None:
            self._steps_required = json['steps_required']
            self._steps_remaining = json['steps_remaining']
            self._hatched = json['hatched']
        else:
            self._steps_required = self._rand_steps()

            # This value is decremented by the walk method until it hatches
            self._steps_remaining = self._steps_required

            self._hatched = False

    @property
    def steps_required(self) -> int:
        """ Gets and returns _steps_required property """
        return self._steps_required

    @property
    def steps_remaining(self) -> int:
        """ Gets and returns _steps_remaining property """
        return self._steps_remaining

    def add_steps(self, steps: int) -> None:
        """ Decrements _steps_remaining by param steps. If _steps_remaining <= 0, _hatched property is set to True.

        :param int steps: Number of steps to decrement _steps_remaining by.
        :return: No return
        :rtype: None

        """
        self._steps_remaining -= steps
        if self._steps_remaining <= 0:
            self._hatched = True

    @property
    def description(self) -> str:
        """ Returns a description of the Egg """
        return f"Your {self._nickname} is {self._height}cm tall and {self._weight}kg. " \
               f"{ 'Currently in party.' if self._in_party else 'Not currently in party'}"

    @property
    def hatched(self) -> bool:
        """ Gets and returns hatched property """
        return self._hatched

    def to_dict(self) -> dict:
        """ Converts current instance attributes into dictionary format and returns it

        :return: Dictionary of all instance attributes
        :rtype: dict

        """
        dik = {
            "id": self._id,
            "member_type": self.member_type(),
            "pokedex_num": self._pokedex_num,
            "source": self._source,
            "nickname":  self._nickname,
            "item": self._item,

            "in_party": self._in_party,
            "weight": self._weight,
            "height": self._height,
            "date_acquired": str(self._date_acquired),

            "steps_required": self._steps_required,
            "steps_remaining": self._steps_remaining,
            "hatched": self._hatched
        }
        return dik

    @classmethod
    def member_type(cls) -> str:
        """ Gets and returns class variable _MEMBER_TYPE

        :return: Member type
        :rtype: String

        """
        return cls._MEMBER_TYPE
    
    @classmethod
    def _rand_steps(cls) -> int:
        """ Class method which calculates a random integer between class variables _MIN_STEPS and _MAX_STEPS """
        return randint(cls._MIN_STEPS, cls._MAX_STEPS)
