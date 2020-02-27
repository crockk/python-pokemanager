"""
Author: Tushya Iyer, Nolan Crooks
ACIT 2515
Date: 2/17/2020
"""
from party_member import PartyMember
from pokedex import Pokedex, Moves
from typing import List
from random import randint, uniform, sample
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

    _MOVE_SET_LENGTH = 4

    _DISPLAY_COLUMN_WIDTH = 14

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

        self._moves = self._rand_move_set()

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

    def use_move(self, move_index: int) -> None:
        """ Uses a move from the move list, if it knows the move

        :return: Message describing move
        :rtype: String

        """
        super()._validate_int(move_index, 1, "Move Index must be an Integer between 1 and 4 inclusive", max_val=4)
        move = self._moves[move_index - 1]
        out_str = f"{self._nickname} used {move[0]}!! it did {move[1]} damage!"
        print(out_str)
        return out_str

    def display_moves(self, move_index: int = None):
        """ Displays all the pokemons moves or a single move in a neat table format
        
        :param: int move_index: the index of the move you want to display
        :return: None
        :rtype: None

        """
        out_str = '\n'

        if move_index is not None:
            super()._validate_int(move_index, 1, "Move Index must be an Integer between 1 and 4 inclusive", max_val=4)
            move = self._moves[move_index - 1]
            out_str += self._display_3_column_line("Move Index", "Move Name", "Damage")
            out_str += ( '=' * (self._DISPLAY_COLUMN_WIDTH * 3 + 2) + '\n')
            out_str += self._display_3_column_line(move_index, move[0], move[1])
            
        else:
            out_str += self._display_3_column_line("Move Index", "Move Name", "Damage")
            out_str += ( '=' * (self._DISPLAY_COLUMN_WIDTH * 3 + 2) + '\n')
            for i in range(len(self._moves)):
                move = self._moves[i]
                out_str += self._display_3_column_line(i + 1, move[0], move[1])  

        print(out_str)
        return out_str

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

    @classmethod
    def member_type(cls):
        """ Gets and returns class variable _MEMBER_TYPE

        :return: Member type
        :rtype: String

        """
        return cls._MEMBER_TYPE

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
    def _rand_move_set(cls):
        """ Randomly selects _MOVE_SET_LENGTH number of moves from the Moves stored in pokedex module

        :return: Move tuple from Moves
        :rtype: Tuple

        """
        move_indices = sample(list(Moves), cls._MOVE_SET_LENGTH)

        return [Moves[move_index] for move_index in move_indices]

    @classmethod
    def _display_3_column_line(cls, col1, col2, col3):
        """ Displays a single row in a 3 column table

        :return: a formatted row in the table
        :rtype: String
        
        """
        return f"{col1}".ljust(cls._DISPLAY_COLUMN_WIDTH) + '|' + f"{col2}".ljust(cls._DISPLAY_COLUMN_WIDTH) + '|' + f"{col3}".ljust(cls._DISPLAY_COLUMN_WIDTH) + '\n'

    def to_dict(self):
        """ Create JSON Object to parse to file

        :return: JSON Object of all properties
        :rtype: Dictionary

        """
        dikt = {
            "id": self._id,
            "pokedex_num": self._pokedex_num,
            "source": self._source,
            "nickname": self._nickname,
            "item": self._item,

            "in_party": self._in_party,
            "weight": self._weight,
            "height": self._height,
            "date_acquired": str(self._date_acquired),

            "ability": self._ability,
            "elemental_type": self._elemental_type,
            "next_level_xp": self._next_level_xp,
            "current_level_xp" :self._current_level_xp,
            "level": self._level,
            "attack": self._attack,
            "speed": self._speed,
            "total_hp": self._total_hp,
            "current_hp": self._current_hp,
            "is_KO": self._is_KO,
            "moves": self._moves
        }
        return dikt
