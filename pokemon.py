"""
Author: Tushya Iyer, Nolan Crooks
ACIT 2515
Date: 2/17/2020
"""

from peewee import CharField, IntegerField, DecimalField, DateField, BooleanField, ForeignKeyField
from party_member import PartyMember
from party_manager import PartyManager
from pokedex import Pokedex, RandomStats
from typing import List, Dict
from random import randint, uniform, sample
from math import ceil
from datetime import date


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


    # _MEMBER_TYPE = "Pokemon"

    # @property
    # def xp_till_next_level(self) -> int:
    #     """ Calculates and returns the Pokemon's xp till next level

    #     :return: Xp left to level up
    #     :rtype: Integer

    #     """
    #     return self._next_level_xp - self._current_level_xp

    # @property
    # def description(self) -> str:
    #     """ Gets and returns a description of the Pokemon

    #     :return: Description of Pokemon
    #     :rtype: String

    #     """
    #     return f"Your {self._nickname} is {self._height}cm tall and {self._weight}kg. \n " \
    #            f"Current level: {self._level}, exp to next level: {self._next_level_xp}. \n" \
    #            f"{'Currently in party.' if self._in_party else 'Not currently in party'}"

    # def use_move(self, move_index: int) -> None:
    #     """ Uses a move from the move list, if it knows the move

    #     :return: Message describing move
    #     :rtype: String

    #     """
    #     super()._validate_int(move_index, 1, "Move Index must be an Integer between 1 and 4 inclusive", max_val=4)
    #     move = self._moves[move_index - 1]
    #     out_str = f"{self._nickname} used {move[0]}!! it did {move[1]} damage!"
    #     print(out_str)
    #     return out_str

    # def display_moves(self, move_index: int = None) -> None:
    #     """ Displays all the pokemons moves or a single move in a neat table format
        
    #     :param: int move_index: the index of the move you want to display
    #     :return: None
    #     :rtype: None

    #     """
    #     out_str = '\n'

    #     if move_index is not None:
    #         super()._validate_int(move_index, 1, "Move Index must be an Integer between 1 and 4 inclusive", max_val=4)
    #         move = self._moves[move_index - 1]
    #         out_str += self._display_3_column_line("Move Index", "Move Name", "Damage")
    #         out_str += ( '=' * (self._DISPLAY_COLUMN_WIDTH * 3 + 2) + '\n')
    #         out_str += self._display_3_column_line(move_index, move[0], move[1])
            
    #     else:
    #         out_str += self._display_3_column_line("Move Index", "Move Name", "Damage")
    #         out_str += ( '=' * (self._DISPLAY_COLUMN_WIDTH * 3 + 2) + '\n')
    #         for i in range(len(self._moves)):
    #             move = self._moves[i]
    #             out_str += self._display_3_column_line(i + 1, move[0], move[1])  

    #     print(out_str)
    #     return out_str

    # def add_xp(self, xp_increase: int) -> None:
    #     """ Adds xp to the Pokemon's current XP level, and levels up if the next level XP is reached

    #     :param: int xp_increase: XP to increase by
    #     :return: No return
    #     :rtype: None

    #     """
    #     super()._validate_int(xp_increase, 1, "XP increase must be an Integer greater than or equal to 1")

    #     if xp_increase + self._current_level_xp > self._next_level_xp:
    #         xp_added = self._next_level_xp - self._current_level_xp
    #         self._level_up()
    #         # are we allowed recursion???
    #         self.add_xp(xp_increase - xp_added)
    #     elif xp_increase + self._current_level_xp == self._next_level_xp:
    #         self._level_up()
    #     else:
    #         self._current_level_xp += xp_increase

    # def heal(self, health_increase: int) -> None:
    #     """ Heals Pokemon based on given increase

    #     :param int health_increase: Amount to heal Pokemon by
    #     :return: No return
    #     :rtype: None

    #     """
    #     super()._validate_int(health_increase, 1, "Health increase must be an Integer greater than or equal to 1")

    #     if health_increase + self._current_hp >= self._total_hp:
    #         self._current_hp = self._total_hp
    #     else:
    #         self._current_hp += health_increase

    # def damage(self, health_decrease: int) -> None:
    #     """ Damages the Pokemon (decreases current HP) by a given value

    #     :param int health_decrease: Amount to decrease health by
    #     :return: No return
    #     :rtype: None

    #     """
    #     super()._validate_int(health_decrease, 1, "Damage must be an Integer greater than or equal to 1")

    #     if self._current_hp - health_decrease <= 0:
    #         self._knock_out()
    #     else:
    #         self._current_hp -= health_decrease

    # def _level_up(self) -> None:
    #     """ Level up the pokemon by 1 and set the current XP to 0

    #     :return: No return
    #     :rtype: None

    #     """

    #     self._level += 1
    #     self._current_level_xp = 0
    #     self._next_level_xp = ceil(self._next_level_xp * self._rand_xp_level_up_multiplier())

    #     print(f"{self._nickname} has leveled up to level {self.level}!!")

    # def _knock_out(self) -> None:
    #     """ Kills the Pokemon

    #     :return: No return
    #     :rtype: None

    #     """
    #     self._is_KO = True
    #     print(f"{self._nickname} was knocked out")

    # def to_dict(self) -> dict:
    #     """ Create JSON Object to parse to file

    #     :return: JSON Object of all properties
    #     :rtype: Dictionary

    #     """
    #     dikt = {
    #         "id": self._id,
    #         "member_type": self.member_type(),
    #         "pokedex_num": self._pokedex_num,
    #         "source": self._source,
    #         "nickname": self._nickname,
    #         "item": self._item,

    #         "in_party": self._in_party,
    #         "weight": self._weight,
    #         "height": self._height,
    #         "date_acquired": str(self._date_acquired),

    #         "ability": self._ability,
    #         "elemental_type": self._elemental_type,
    #         "next_level_xp": self._next_level_xp,
    #         "current_level_xp" :self._current_level_xp,
    #         "level": self._level,
    #         "attack": self._attack,
    #         "speed": self._speed,
    #         "total_hp": self._total_hp,
    #         "current_hp": self._current_hp,
    #         "is_KO": self._is_KO,
    #         "moves": self._moves
    #     }
    #     return dikt

    next_level_xp = IntegerField(column_name='next_level_xp', default=RandomStats.rand_base_xp)
    current_level_xp = IntegerField(column_name='current_level_xp', default=0)
    level = IntegerField(column_name='level', default=5)
    ability = CharField(column_name='ability', null=True)
    attack = IntegerField(column_name='attack', default=RandomStats.rand_battle_stat())
    speed = IntegerField(column_name='speed', default=RandomStats.rand_battle_stat())
    defense = IntegerField(column_name='defense', default=RandomStats.rand_battle_stat)
    total_hp = IntegerField(column_name='total_hp', default=RandomStats.rand_base_xp)
    current_hp = IntegerField(column_name='current_hp', default=total_hp)
    is_KO = BooleanField(default=False)
    member_type = CharField(column_name='member_type', default='Pokemon')
    player = ForeignKeyField(PartyManager, backref='pokemon')