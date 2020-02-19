"""
Author: Tushya Iyer, Nolan Crooks
ACIT 2515
Date: 2/13/2020
"""

from party_member import PartyMember
from pokemon import Pokemon
from egg import Egg
from poke_stats import PokeStats
from typing import List


class PartyManager:
    _POKEDEX = {
        1: "Bulbasaur",
        2: "Charmander",
        3: "Squirtle",
        4: "Pikachu",
        5: "Turtwig",
        6: "Chimchar",
        7: "Piplup",
        8: "Kyogre",
        9: "Groudon",
        10: "Rayquaza"
    }

    _ID = 1

    def __init__(self, player_name: str) -> None:
        
        self._validate_string(player_name, "Player Name must be a non blank String")

        self._party = {}
        self._pc_pokemon = {}
        self._player_name = player_name

    def add_party_member(self, member_type: str, pokedex_num: int, source: str, nickname: str = None, item: str = None, ability: str = None) -> None:

        if member_type == Pokemon.member_type():
            self._pc_pokemon[self._ID] = Pokemon(self._ID, pokedex_num, source, nickname=nickname, item=item, ability=ability)
            self._ID += 1        
        elif member_type == Egg.member_type():
            self._pc_pokemon[self._ID] = Egg(self._ID, pokedex_num, source, nickname=nickname, item=item)
            self._ID += 1
        else:
            print(f"{member_type} is not a valid Party Member type")

    def withdraw_party_member(self, id: int) -> None:
        pass

    def release_party_member(self, id: int) -> None:
        pass

    def get_members_by_types(self, type: tuple) -> List:
        pass

    def get_member_by_id(self, id: int) -> PartyMember:
        return self._party[id]

    def get_stats(self) -> PokeStats:
        pass

    @staticmethod
    def _validate_string(string: str, error_msg: str) -> None:
        """Private method. Used to validate strings according to type. Raises an error with a custom error message"""
        if type(string) is not str:
            raise TypeError(error_msg + f"\nNot type {type(string)}")
        if not string:
            raise ValueError(error_msg)