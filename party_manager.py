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
import random
from pokedex import Pokedex
import os
import json
from datetime import date, datetime


class PartyManager:
    """ Defines the manager class PartyManager

    This class manages one player's Pokemon Party and PC Storage (PC Storage is where Pokemon that are not in a party
    are placed).

    CLASS VARIABLES
    _POKEDEX: Object containing an integer as a key, and a tuple containing species and type as the value.
    This is used to assign a Pokedex number and allows us to determine the species/type based upon that number.    

    """
    random.seed(13)

    _POKEDEX = Pokedex

    _DISPLAY_COLUMN_WIDTH = 24

    _DATA_DIRECTORY = "data"
    _DATA_FILENAME = "pokedata.json"

    def __init__(self, player_name: str) -> None:
        """ Initializes the instance properties

        In addition to setting the player name, this __init__ also sets up _party and _pc_pokemon properties
        as empty objects, which will be populated as the user adds Pokemon to his or her party or storage.

        _ID: A unique identifier given to each party member, is incremented by 1 each time a new
        party member is created.

        :param str player_name: The player's name.
        :return: No return
        :rtype: None

        """
        self._filepath = os.path.join(self._DATA_DIRECTORY, self._DATA_FILENAME)

        if os.path.exists(self._filepath):
                self._read_from_file()
        else:
            self._validate_string(player_name, "Player Name must be a non blank String")

            self._ID = 1
            self._player_name = player_name
            self._party = {}
            self._pc_pokemon = {}
            self._total_steps = 0

        self._write_to_file()

    def _read_from_file(self):
        with open(self._filepath, "r") as file:
            manager = json.load(file)
            self._ID = manager["ID_count"]
            self._player_name = manager["player_name"]
            self._party = {}
            self._pc_pokemon = {}
            for member in manager["party"]:
                self.create_member(
                    member["member_type"],
                    member["pokedex_num"],
                    member["source"],
                    member["nickname"],
                    member["item"],
                    # id=member["id"],

                )
                if member["in_party"]:
                    self.move_to_party(member["id"])

            self._total_steps = manager["total_steps"]

    def _write_to_file(self):
        data = self.to_dict()
        with open(self._filepath, "w") as file:
            json.dump(data, file)

    def to_dict(self):
        dik = {
            "ID_count": self._ID,
            "party": [member.to_dict() for member in self._party.values()],
            "pc_pokemon": [member.to_dict() for member in self._pc_pokemon.values()],
            "player_name": self._player_name,
            "total_steps": self._total_steps,
            "filepath": self._filepath
        }
        return dik

    def create_member(self, member_type: str, pokedex_num: int, source: str, nickname: str = None, item: str = None, ability: str = None) -> None:
        """ Adds a member (egg or Pokemon) to the player's _pc.

        Depending on the type of member, this function adds a new entry to the player's party. It also assigns the
        Pokemon an ID, and then increments it by 1 so that it is unique for the next member that is added.

        :param member_type: The party member type, either "Egg" or "Pokemon"
        :param pokedex_num: The Pokedex number that corresponds with the Pokemon species.
        :param source: The location that the Pokemon/Egg was acquired.
        :param nickname: The given name for the Pokemon.
        :param item: The item that the Pokemon is currently holding.
        :param ability: The Pokemon's special ability.
        :return: No return
        :rtype: None

        """
        self._validate_pokedex_number(pokedex_num)

        if not nickname:
            nickname = self._POKEDEX[pokedex_num][0]

        if member_type == Pokemon.member_type():
            self._pc_pokemon[self._ID] = Pokemon(self._ID, pokedex_num, source, nickname=nickname, item=item, ability=ability)
            self._ID += 1
        elif member_type == Egg.member_type():
            self._pc_pokemon[self._ID] = Egg(self._ID, pokedex_num, source, nickname=nickname, item=item)
            self._ID += 1
        else:
            raise ValueError(f"{member_type} is not a valid Party Member type")
        
        self._write_to_file()

    def move_to_party(self, id: int) -> bool:
        """ Moves a pokemon from the PC storage into the party

        :param int id: Pokemon's ID
        :return: Boolean for testing
        :rtype: Boolean

        """
        if len(self._party) < 6:
            pokemon = self._pc_pokemon[id]
            self._party[id] = pokemon
            self._party[id]._in_party = True
            self.release_pc_pokemon(id)
            
            self._write_to_file()

            return True
        else:
            print('Your party is full')
            return False

    def move_to_pc(self, id: int) -> bool:
        """ Removes a party member from _party and places it into _pc_storage.

        :param int id: The ID of the Pokemon or Egg to be placed into storage.
        :return: Boolean for testing
        :rtype: Boolean

        """
        if id in self._party.keys():
            self._pc_pokemon[id] = self._party[id]
            del self._party[id]
            
            self._write_to_file()

            return True
        else:
            return False

    def release_party_member(self, id: int) -> bool:
        """ Releases a party member from _party back into the wilderness :'(

        :param int id: The ID of the Pokemon or Egg to be released.
        :return: Bool for testing
        :rtype: Boolean

        """
        if id in self._party.keys():
            del self._party[id] # pokemon has been yeeted

            self._write_to_file()

            return True
        else:
            return False

    def release_pc_pokemon(self, id: int) -> bool:
        """ Releases a pokemon stored in _pc_pokemon back into the wilderness :'(

        :param int id: The ID of the Pokemon or Egg to be released.
        :return: Bool for testing
        :rtype: Boolean

        """
        if id in self._pc_pokemon.keys():
            del self._pc_pokemon[id] # pokemon has been yeeted

            
            self._write_to_file()

            return True
        else:
            return False
    
    def walk(self, steps: int):
        """ Player walks a given amount of steps, which is added to the steps of all eggs in party. Hatches eggs
        if necessary

         :param int steps: Steps to walk
         :return: No return
         :rtype: None

         """
        eggs = self.get_member_by_type('Egg')

        for egg in eggs:
            if egg.in_party:
                egg.add_steps(steps)
                if egg.hatched:
                    temp_egg = egg
                    self.release_party_member(egg.id)
                    self.create_member("Pokemon", temp_egg.pokedex_num, temp_egg.source, temp_egg.nickname)
                    self.move_to_party(self._ID - 1)

        self._total_steps += steps
        
        self._write_to_file()

    def get_members_by_elemental_type(self, types: tuple) -> dict:
        """ Gets a collection of party members based on a given elemental type or types.

        :param tuple types: A tuple containing the desired types.
        :return: Returns a collection of desired types from the party, seperated by type
        :rtype: Dictionary

        """
        members = {}
        all_members = list(self._pc_pokemon.values()) + list(self._party.values())

        for member in all_members:
            if member.member_type == Pokemon.member_type:
                for e_type in member.elemental_type:
                    if e_type in types:
                        if e_type in members:
                            members[e_type].append(member)
                        else:
                            members[e_type] = [member]

        return members

    def get_all_members_by_elemental_type(self) -> dict:
        """ Gets a collection of party members based on types

        :return: Returns a collection of desired types from the party, seperated by type
        :rtype: Dictionary

        """
        members = {}
        all_members = list(self._pc_pokemon.values()) + list(self._party.values())

        for member in all_members:
            if member.member_type == Pokemon.member_type:
                for e_type in member.elemental_type:
                    if e_type in members:
                        members[e_type].append(member)
                    else:
                        members[e_type] = [member]

        return members

    def get_member_by_id(self, id: int) -> PartyMember:
        """ Gets a single member from the party based on id.

        :param int id: The ID of the party member to be retrieved.
        :return: Returns the party member object (Pokemon or Egg) based on the given ID.
        :rtype: Pokemon or Egg

        """
        if id in self._party.keys():    
            return self._party[id]
        elif id in self._pc_pokemon.keys():
            return self._pc_pokemon[id]
        else:
            return None

    @property
    def get_all_party_members(self) -> List:
        """ Gets all party members and puts them into a list

        :return: All party members
        :rtype: List

        """
        return list(self._party.values())

    @property
    def get_all_pc_members(self) -> List:
        """ Gets all pc members and puts them into a list

        :return: All party members
        :rtype: List

        """
        return list(self._pc_pokemon.values())

    @property
    def get_all_members(self) -> List:
        """ Gets all party members and puts them into a list

        :return: All party members
        :rtype: List

        """
        return list(self._pc_pokemon.values()) + list(self._party.values())

    def get_member_by_type(self, type: str) -> List:
        """ Gets a list of members from pc_storage and party based on indicated type

        :param str type: The type to filter by
        :return: List of members
        :rtype: List

        """

        all_members = list(self._pc_pokemon.values()) + list(self._party.values())
        members = []
        for member in all_members:
            if member.member_type() == type:
                members.append(member)
        return members

    def display_members(self) -> None:
        """ Displays all the members beloning to the Part Manager in a neat table format

        :return: None
        :rtype: None

        """
        members = self.get_all_members

        print(self._display_4_column_line("Manager ID", "Nickname", "Elemental Type", "Member Type"))
        print( '=' * (self._DISPLAY_COLUMN_WIDTH * 4 + 3) )
        for member in members:
            if member.member_type() == Pokemon.member_type():
                print(self._display_4_column_line(member.id, member.nickname, ','.join(member.elemental_type), member.member_type()))
            else:
                print(self._display_4_column_line(member.id, member.nickname, 'Unknown', member.member_type()))


    def get_stats(self) -> PokeStats:
        """ Populates a stats object with statistics about the party manager """
        all_members = list(self._pc_pokemon.values()) + list(self._party.values())

        members_by_type = self.get_all_members_by_elemental_type()
        total_eggs = len(self.get_member_by_type('Egg'))
        total_KO = 0
        total_steps = self._total_steps

        for member in all_members:
            if member.member_type() == 'Pokemon' and member.is_KO:
                total_KO += 1

        return PokeStats(members_by_type, total_eggs, total_KO, total_steps)
    
    @staticmethod
    def _validate_string(string: str, error_msg: str) -> None:
        """ Private method. Used to validate strings according to type. Raises an error with a custom error message.

        :param str string: The string to be validated
        :param str error_msg: The error message to be returned if an exception is raised.
        :return: No return
        :rtype: none
        """
        if type(string) is not str:
            raise TypeError(error_msg + f"\nNot type {type(string)}")
        if not string:
            raise ValueError(error_msg)

    def _validate_pokedex_number(self, pokedex_num:int) -> None:
        """ Checks to see if the given pokedex number corrisponds to a pokedex entry """
        if pokedex_num not in self._POKEDEX.keys():
            raise ValueError(f'Pokedex Number must be between 1 - {len(self._POKEDEX) + 1}')

    @classmethod
    def _display_4_column_line(cls, col1, col2, col3, col4):
        """ Displays a single row in a 4 column table

        :return: a formatted row in the table
        :rtype: String
        
        """
        out_str = ''
        out_str += f"{col1}".ljust(cls._DISPLAY_COLUMN_WIDTH) + '|' + f"{col2}".ljust(cls._DISPLAY_COLUMN_WIDTH)
        out_str += '|' + f"{col3}".ljust(cls._DISPLAY_COLUMN_WIDTH) + '|' + f"{col4}".ljust(cls._DISPLAY_COLUMN_WIDTH)

        return out_str
