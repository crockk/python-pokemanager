"""
Author: Tushya Iyer, Nolan Crooks
ACIT 2515
Date: 2/13/2020
"""

from peewee import IntegerField, CharField
from db import BaseModel
from poke_stats import PokeStats
from typing import List, Dict
import random
from pokedex import Pokedex
import os
import json
from datetime import date, datetime


class PartyManager(BaseModel):
    pass
    """ Defines the manager class PartyManager
    This class manages one player's Pokemon Party and PC Storage (PC Storage is where Pokemon that are not in a party
    are placed).
    CLASS VARIABLES
    _POKEDEX: Object containing an integer as a key, and a tuple containing species and type as the value.
    This is used to assign a Pokedex number and allows us to determine the species/type based upon that number.    
    """
    player_name = CharField(null=False)
    total_steps = IntegerField(default=0)
    random.seed(13)
    _POKEDEX = Pokedex

    # IT'S ALL OBSOLETE BAYBEE WOOOOOO SHOULDA DONE DB FROM THE VERY START WOOOO USELESS CODE

    # def create_member(self, member_type: str, pokedex_num: int, source: str, nickname: str = None, item: str = None, ability: str = None, json: Dict = None) -> int:
    #     self._validate_pokedex_number(pokedex_num)
    #     if not nickname:
    #         nickname = self._POKEDEX[pokedex_num][0]
    #     if member_type == Pokemon.member_type():
    #         self._pc_pokemon[self._ID] = Pokemon(self._ID, pokedex_num, source, nickname=nickname, item=item, ability=ability, json=json)
    #         self._ID += 1
    #     elif member_type == Egg.member_type():
    #         self._pc_pokemon[self._ID] = Egg(self._ID, pokedex_num, source, nickname=nickname, item=item, json=json)
    #         self._ID += 1
    #     else:
    #         raise ValueError(f"{member_type} is not a valid Party Member type")
      
    #     self._write_to_file()
    #     return self._ID - 1
    
    # def move_to_party(self, id: int) -> bool:
    #     """ Moves a pokemon from the PC storage into the party
    #     :param int id: Pokemon's ID
    #     :return: Boolean for testing
    #     :rtype: Boolean
    #     """
    #     if len(self._party) >= 6:
    #         print('Your party is full')
    #         return False
    #     elif id in self._party:
    #         print(f"This {self._party[id].member_type} is already in your party!")
    #         return False
    #     elif id not in self._pc_pokemon:
    #         print("This pokemon is not available")
    #         return False
    #     else:
    #         pokemon = self._pc_pokemon[id]
    #         self._party[id] = pokemon
    #         self._party[id]._in_party = True
    #         self.release_pc_pokemon(id)
          
    #         self._write_to_file()
    #         return True
    # def move_to_pc(self, id: int) -> bool:
    #     """ Removes a party member from _party and places it into _pc_storage.
    #     :param int id: The ID of the Pokemon or Egg to be placed into storage.
    #     :return: Boolean for testing
    #     :rtype: Boolean
    #     """
    #     if id in self._party.keys():
    #         self._pc_pokemon[id] = self._party[id]
    #         del self._party[id]
          
    #         self._write_to_file()
    #         return True
    #     else:
    #         return False
    # def release_party_member(self, id: int) -> bool:
    #     """ Releases a party member from _party back into the wilderness :'(
    #     :param int id: The ID of the Pokemon or Egg to be released.
    #     :return: Bool for testing
    #     :rtype: Boolean
    #     """
    #     if id in self._party.keys():
    #         del self._party[id] # pokemon has been yeeted
    #         self._write_to_file()
    #         return True
    #     else:
    #         return False
    # def release_pc_pokemon(self, id: int) -> bool:
    #     """ Releases a pokemon stored in _pc_pokemon back into the wilderness :'(
    #     :param int id: The ID of the Pokemon or Egg to be released.
    #     :return: Bool for testing
    #     :rtype: Boolean
    #     """
    #     if id in self._pc_pokemon.keys():
    #         del self._pc_pokemon[id] # pokemon has been yeeted
          
    #         self._write_to_file()
    #         return True
    #     else:
    #         return False
  
    # def walk(self, steps: int) -> None:
    #     """ Player walks a given amount of steps, which is added to the steps of all eggs in party. Hatches eggs
    #     if necessary
    #      :param int steps: Steps to walk
    #      :return: No return
    #      :rtype: None
    #      """
    #     eggs = self.get_member_by_type('Egg')
    #     for egg in eggs:
    #         if egg.in_party:
    #             egg.add_steps(steps)
    #             if egg.hatched:
    #                 temp_egg = egg
    #                 self.release_party_member(egg.id)
    #                 self.create_member("Pokemon", temp_egg.pokedex_num, temp_egg.source, temp_egg.nickname)
    #                 self.move_to_party(self._ID - 1)
    #     self._total_steps += steps
      
    #     self._write_to_file()
    # def add_xp_to_pokemon(self, id: int, xp: int) -> None:
    #     """ Adds a specified amount of experience points to a given PartyMember
    #     :param id: The PartyMember to add xp to
    #     :param xp: Amount of xp to add
    #     :return: No return
    #     :rtype: None
    #     """
    #     self.get_member_by_id(id).add_xp(xp)
    #     self._write_to_file()
    # def get_members_by_elemental_type(self, types: tuple) -> dict:
    #     """ Gets a collection of party members based on a given elemental type or types.
    #     :param tuple types: A tuple containing the desired types.
    #     :return: Returns a collection of desired types from the party, seperated by type
    #     :rtype: Dictionary
    #     """
    #     members = {}
    #     all_members = list(self._pc_pokemon.values()) + list(self._party.values())
    #     for member in all_members:
    #         if member.member_type == Pokemon.member_type:
    #             for e_type in member.elemental_type:
    #                 if e_type in types:
    #                     if e_type in members:
    #                         members[e_type].append(member)
    #                     else:
    #                         members[e_type] = [member]
    #     return members
    # def get_all_members_by_elemental_type(self) -> dict:
    #     """ Gets a collection of party members based on types
    #     :return: Returns a collection of desired types from the party, seperated by type
    #     :rtype: Dictionary
    #     """
    #     members = {}
    #     all_members = list(self._pc_pokemon.values()) + list(self._party.values())
    #     for member in all_members:
    #         if member.member_type == Pokemon.member_type:
    #             for e_type in member.elemental_type:
    #                 if e_type in members:
    #                     members[e_type].append(member)
    #                 else:
    #                     members[e_type] = [member]
    #     return members
    # def get_member_by_id(self, id: int) -> PartyMember:
    #     """ Gets a single member from the party based on id.
    #     :param int id: The ID of the party member to be retrieved.
    #     :return: Returns the party member object (Pokemon or Egg) based on the given ID.
    #     :rtype: Pokemon or Egg
    #     """
    #     if id in self._party.keys():    
    #         return self._party[id]
    #     elif id in self._pc_pokemon.keys():
    #         return self._pc_pokemon[id]
    #     else:
    #         return None
    # def get_member_by_type(self, type: str) -> List:
    #     """ Gets a list of members from pc_storage and party based on indicated type
    #     :param str type: The type to filter by
    #     :return: List of members
    #     :rtype: List
    #     """
    #     all_members = list(self._pc_pokemon.values()) + list(self._party.values())
    #     members = []
    #     for member in all_members:
    #         if member.member_type() == type:
    #             members.append(member)
    #     return members
    # def get_stats(self) -> PokeStats:
    #     """ Populates a stats object with statistics about the party manager
    #     :return: PokeStats object
    #     :rtype: PokeStats
    #     """
    #     all_members = list(self._pc_pokemon.values()) + list(self._party.values())
    #     members_by_type = self._total_per_elemental_type()
    #     total_eggs = len(self.get_member_by_type('Egg'))
    #     total_KO = 0
    #     total_steps = self._total_steps
    #     for member in all_members:
    #         if member.member_type() == 'Pokemon' and member.is_KO:
    #             total_KO += 1
    #     return PokeStats(members_by_type, total_eggs, total_KO, total_steps)
    # def _total_per_elemental_type(self) -> dict:
    #     """ Populates and returns a dictionary of total amount of members by each elemental type, eg:
    #         {'Grass': 5, 'Fire': 1}
    #     :return: Dictionary of totals
    #     :rtype: dict
    #     """
    #     members_by_type = self.get_all_members_by_elemental_type()
    #     return {k:len(v) for k,v in members_by_type.items()}
