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
    """ Defines the manager class PartyManager

    This class manages one player's Pokemon Party and PC Storage (PC Storage is where Pokemon that are not in a party
    are placed).

    CLASS VARIABLES
    _POKEDEX: Object containing an integer as a key, and a Pokemon species as a value. This is used to assign
              a pokedex number and allows us to determine the species based upon that number.

    _ID: A unique identifier given to each party member, is incremented by 1 each time a new
         party member is created.

    """

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
        """ Initializes the instance properties

        In addition to setting the player name, this __init__ also sets up _party and _pc_pokemon properties
        as empty objects, which will be populated as the user adds Pokemon to his or her party or storage.

        :param str player_name: The player's name.
        :return: No return
        :rtype: None

        """
        self._validate_string(player_name, "Player Name must be a non blank String")

        self._party = {}
        self._pc_pokemon = {}
        self._player_name = player_name

    def add_party_member(self, member_type: str, pokedex_num: int, source: str, nickname: str = None, item: str = None, ability: str = None) -> None:
        # Add check to see if there are already 6 pokemon in party?
        """ Adds a member (egg or Pokemon) to the player's _party.

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

        if member_type == Pokemon.member_type():
            self._pc_pokemon[self._ID] = Pokemon(self._ID, pokedex_num, source, nickname=nickname, item=item, ability=ability)
            self._ID += 1        
        elif member_type == Egg.member_type():
            self._pc_pokemon[self._ID] = Egg(self._ID, pokedex_num, source, nickname=nickname, item=item)
            self._ID += 1
        else:
            print(f"{member_type} is not a valid Party Member type")

    def withdraw_party_member(self, id: int) -> None:
        """ Removes a party member from _party and places it into _pc_storage.

        :param int id: The ID of the Pokemon or Egg to be placed into storage.
        :return: No return
        :rtype: None

        """
        self._pc_pokemon[id] = self._party[id]
        del self._party[id]

    def release_party_member(self, id: int) -> None:
        """ Releases a party member from _party back into the wilderness :'(

        :param int id: The ID of the Pokemon or Egg to be released.
        :return: No return
        :rtype: None

        """
        del self._party[id] # pokemon has been yeeted

    def release_pc_pokemon(self, id: int) -> None:
        """ Releases a pokemon stored in _pc_pokemon back into the wilderness :'(

        :param int id: The ID of the Pokemon or Egg to be released.
        :return: No return
        :rtype: None

        """
        del self._pc_pokemon[id] # pokemon has been yeeted

    def get_members_by_types(self, types: tuple) -> dict:
        """ Gets a collection of party members based on a given type or types.

        :param tuple types: A tuple containing the desired types.
        :return: Returns a collection of desired types from the party, seperated by type
        :rtype: Dictionary

        """
        members = {}
        for type in types:
            members[type] = []
            for key in self._party.keys():
                if self._party[key].member_type == type:
                    members[key].append(self._party[key])
        return members

    def get_member_by_id(self, id: int) -> PartyMember:
        """ Gets a single member from the party based on id.

        :param int id: The ID of the party member to be retrieved.
        :return: Returns the party member object (Pokemon or Egg) based on the given ID.
        :rtype: Pokemon or Egg

        """
        return self._party[id]

    def get_stats(self) -> PokeStats:
        pass

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