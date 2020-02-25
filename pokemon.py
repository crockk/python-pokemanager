"""
Author: Tushya Iyer, Nolan Crooks
ACIT 2515
Date: 2/17/2020
"""
from party_member import PartyMember
from pokedex import Pokedex
from typing import List
from random import randint, uniform
from math import ceil


class Pokemon(PartyMember):
    """ Defines the subclass Pokemon which is a child of PartyMember

    This class inherits all properties of PartyMember, and adds many stats and attributes.

    CLASS VARIABLES:
    _MEMBER_TYPE: The type of party member. In this case, it is "Pokemon"

    _MIN_BASE_XP and _MAX_BASE_XP: Defines range for base XP to be generated

    _MIN_LEVEL_UP_XP_MULT and _MAX_LEVEL_UP_XP_MULT: Defines range for level up multiplier

    _STARTING_LEVEL: Starting level for the pokemon

    _MIN_BATTLE_STAT and _MAX_BATTLE_STAT: Defines range for battle stats to be generated

    _MIN_BASE_HP and _MAX_BASE_HP: Defines range for base HP to be generated

    """

    _MEMBER_TYPE = "Pokemon"

    _MIN_BASE_XP = 80
    _MAX_BASE_XP = 120

    _MIN_LEVEL_UP_XP_MULT = 1.0
    _MAX_LEVEL_UP_XP_MULT = 1.5

    _STARTING_LEVEL = 5

    _MIN_BATTLE_STAT = 3
    _MAX_BATTLE_STAT = 18

    _MIN_BASE_HP = 15
    _MAX_BASE_HP = 35

    def __init__(self, id: int, pokedex_num: int, source: str, nickname: str = None, item: str = None,
                 ability: str = None) -> None:
        """ Initializes the instance properties

        :param int id: Automatically assigned id (incremented each time a new Pokemon or egg is created)
        :param int pokedex_num: The Pokedex number of the Pokemon
        :param str source: The location where the Pokemon was acquired.
        :param str nickname: The Pokemon's given name
        :param str item: The item held by the Pokemon
        :param str ability: The Pokemon's special ability
        :return: No return
        :rtype: None

        """

        super().__init__(id, pokedex_num, source, nickname, item)

        if ability is not None:
            super()._validate_string(ability, "Ability must be a none-blank String")

        types = Pokedex[pokedex_num][1].split('/')
        for e_type in types:
            super()._validate_string(e_type, "Elemental Type must be a none-blank String")

        self._ability = ability

        self._elemental_type = tuple(types)

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
        """ Gets and returns property id

        :return: ID
        :rtype: Integer

        """
        return self._id

    @property
    def moves(self) -> List:
        """ Gets and returns this pokemon's move list

        :return: Pokemon moves
        :rtype: List

        """
        return self._moves

    @property
    def xp_till_next_level(self) -> int:
        """ Calculates and returns the Pokemon's xp till next level

        :return: Xp left to level up
        :rtype: Integer

        """
        return self._next_level_xp - self._current_level_xp

    @property
    def level(self) -> int:
        """ Gets and returns Pokemon's current level

        :return: Level
        :rtype: Integer

        """
        return self._level

    @property
    def ability(self) -> str:
        """ Gets and returns existing ability, if any

        :return: Ability
        :rtype: String

        """
        if self._ability:
            return self._ability
        else:
            return "None"

    @property
    def elemental_type(self) -> tuple:
        """ Gets and returns the Pokemon's type(s)

        :return: Types
        :rtype: Tuple

        """
        return self._elemental_type

    @property
    def attack(self) -> int:
        """ Gets and returns Pokemon's attack stat

        :return: Attack stat
        :rtype: Integer

        """
        return self._attack

    @property
    def speed(self) -> int:
        """ Gets and returns Pokemon's speed stat

        :return: Speed stat
        :rtype: Integer

        """
        return self._speed

    @property
    def defense(self) -> int:
        """ Gets and returns Pokemon's defense stat

        :return: Defence stat
        :rtype: Integer

        """
        return self._defense

    @property
    def total_hp(self) -> int:
        """ Gets and returns Pokemon's total HP stat

        :return: Total HP stat
        :rtype: Integer

        """
        return self._total_hp

    @property
    def current_hp(self) -> int:
        """ Gets and returns Pokemon's current HP stat

        :return: Current HP stat
        :rtype: Integer

        """
        return self._current_hp

    @property
    def is_KO(self) -> bool:
        """ Gets and returns is_KO stat

        :return: If pokemone is KO or not
        :rtype: Boolean

        """
        return self._is_KO

    @property
    def description(self) -> str:
        """ Gets and returns a description of the Pokemon

        :return: Description of Pokemon
        :rtype: String

        """
        return f"Your {self._nickname} is {self._height}cm tall and {self._weight}kg. \n " \
               f"Current level: {self._level}, exp to next level: {self._next_level_xp}. \n" \
               f"{'Currently in party.' if self._in_party else 'Not currently in party'}"

    def use_move(self, move: str) -> None:
        """ Uses a move from the move list, if it knows the move

        :return: Message describing move
        :rtype: String

        """
        pass

    def add_xp(self, xp_increase: int) -> None:
        """ Adds xp to the Pokemon's current XP level, and levels up if the next level XP is reached

        :param: int xp_increase: XP to increase by
        :return: No return
        :rtype: None

        """
        super()._validate_int(xp_increase, 1, "XP increase must be an Integer greater than or equal to 1")

        if xp_increase + self._current_level_xp > self._next_level_xp:
            xp_added = self._next_level_xp - self._current_level_xp
            self._level_up()
            # are we allowed recursion???
            self.add_xp(xp_increase - xp_added)
        elif xp_increase + self._current_level_xp == self._next_level_xp:
            self._level_up()
        else:
            self._current_level_xp += xp_increase

    def heal(self, health_increase: int) -> None:
        """ Heals Pokemon based on given increase

        :param int health_increase: Amount to heal Pokemon by
        :return: No return
        :rtype: None

        """
        super()._validate_int(health_increase, 1, "Health increase must be an Integer greater than or equal to 1")

        if health_increase + self._current_hp >= self._total_hp:
            self._current_hp = self._total_hp
        else:
            self._current_hp += health_increase

    def damage(self, health_decrease: int) -> None:
        """ Damages the Pokemon (decreases current HP) by a given value

        :param int health_decrease: Amount to decrease health by
        :return: No return
        :rtype: None

        """
        super()._validate_int(health_decrease, 1, "Damage must be an Integer greater than or equal to 1")

        if self._current_hp - health_decrease <= 0:
            self._knock_out()
        else:
            self._current_hp -= health_decrease

    def _level_up(self) -> None:
        """ Level up the pokemon by 1 and set the current XP to 0

        :return: No return
        :rtype: None

        """

        self._level += 1
        self._current_level_xp = 0
        self._next_level_xp = ceil(self._next_level_xp * self._rand_xp_level_up_multiplier())

        print(f"{self._nickname} has leveled up to level {self.level}!!")

    def _knock_out(self) -> None:
        """ Kills the Pokemon

        :return: No return
        :rtype: None

        """
        self._is_KO = True
        print(f"{self._nickname} was knocked out")

    @classmethod
    def _rand_base_xp(cls) -> int:
        """ Generates random base xp based on class variables

        :return: Base xp level
        :rtype: Integer

        """
        return randint(cls._MIN_BASE_XP, cls._MAX_BASE_XP)

    @classmethod
    def _rand_xp_level_up_multiplier(cls) -> float:
        """ Generates xp level up multiplier based on class variables

        :return: Xp level up multiplier
        :rtype: Float

        """
        return round(uniform(cls._MIN_LEVEL_UP_XP_MULT, cls._MAX_LEVEL_UP_XP_MULT), 2)

    @classmethod
    def _rand_battle_stat(cls) -> int:
        """ Generates random base battle stat based on class variables

        :return: Base stat
        :rtype: Integer

        """
        return randint(cls._MIN_BATTLE_STAT, cls._MAX_BATTLE_STAT)

    @classmethod
    def _rand_base_hp(cls) -> int:
        """ Generates random base HP based on class variables

        :return: Base HP
        :rtype: Integer

        """
        return randint(cls._MIN_BASE_HP, cls._MAX_BASE_HP)

    @classmethod
    def member_type(cls):
        """ Gets and returns class variable _MEMBER_TYPE

        :return: Member type
        :rtype: String

        """
        return cls._MEMBER_TYPE
