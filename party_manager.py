"""
Author: Tushya Iyer, Nolan Crocks
ACIT 2515
Date: 2/13/2020
"""

from party_member import PartyMember
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

    def __init__(self, player_name: str) -> None:
        pass

    def add_party_member(self, new_member: PartyMember) -> None:
        pass

    def withdraw_party_member(self, id: int) -> None:
        pass

    def release_party_member(self, id: int) -> None:
        pass

    def get_members_by_types(self, type: tuple) -> List:
        pass

    def get_member_by_id(self, id: int) -> PartyMember:
        pass

    def get_stats(self) -> PokeStats:
        pass