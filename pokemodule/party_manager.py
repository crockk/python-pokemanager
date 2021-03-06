"""
Author: Tushya Iyer, Nolan Crooks
ACIT 2515
Date: 2/13/2020
"""

from peewee import IntegerField, CharField
from db.db import BaseModel
import random
from pokemodule.pokedex import Pokedex, IdManager
from typing import List
from pokemodule.pokestats import PokeStats


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
    _ID_MANAGER = IdManager()

    @classmethod
    def get_by_id(cls, id: int):
        result = [pm for pm in  cls.select()[:] if pm.id == id]
        if result:
            return result[0]

    @property
    def pc_members(self):
        pc = {m.id:m for m in self.all_members if not m.in_party}
        return pc
    
    @property
    def party_members(self):
        party = {m.id:m for m in self.all_members if m.in_party}
        return party
    
    @property
    def all_members(self):
        return self.pokemon[:] + self.eggs[:]
    
    def move_to_party(self, id: int) -> bool:
        """ Moves a pokemon from the PC storage into the party
        :param int id: Pokemon's ID
        :return: Boolean for testing
        :rtype: Boolean
        """
        if len(self.party_members) >= 6:
            print('Your party is full')
            return False
        elif id in self.party_members:
            print(f"This {self.get_member_by_id(id).member_type} is already in your party!")
            return False
        elif id not in self.pc_members:
            print("This pokemon is not available")
            return False
        else:
            member = [p for p in self.all_members if p.id == id][0]
            member.in_party = True
            member.save()
            return True

    def move_to_pc(self, id: int) -> bool:
        """ Removes a party member from _party and places it into _pc_storage.
        :param int id: The ID of the Pokemon or Egg to be placed into storage.
        :return: Boolean for testing
        :rtype: Boolean
        """
        if id in self.party_members:
            member = [p for p in self.all_members if p.id == id][0]
            member.in_party = False
            member.save()
            return True
        else:
            return False

    def release_member(self, id: str) -> bool:
        """ Releases a party member from pc or party back into the wilderness :'(
        :param int id: The ID of the Pokemon or Egg to be released.
        :return: Bool for testing
        :rtype: Boolean
        """
        members = {m.id:m for m in self.all_members}
        if id in members.keys():
            members[id].delete_instance() # pokemon has been yeeted
            return True
        else:
            return False

    def walk(self, steps: int) -> None:
        """ Player walks a given amount of steps, which is added to the steps of all eggs in party. Hatches eggs
        if necessary
         :param int steps: Steps to walk
         :return: No return
         :rtype: None
         """
        eggs = self.get_member_by_type("Egg")
        for egg in eggs:
            if egg.in_party:
                egg.add_steps(steps)
        self.total_steps += steps
      
        self.save()

    def add_xp_to_pokemon(self, id: int, xp: int) -> None:
        """ Adds a specified amount of experience points to a given PartyMember
        :param id: The PartyMember to add xp to
        :param xp: Amount of xp to add
        :return: No return
        :rtype: None
        """
        self.get_member_by_id(id).add_xp(xp)
    
    def get_members_by_elemental_type(self, types: tuple) -> dict:
        """ Gets a collection of party members based on a given elemental type or types.
        :param tuple types: A tuple containing the desired types.
        :return: Returns a collection of desired types from the party, seperated by type
        :rtype: Dictionary
        """
        members = {}
        for member in self.pokemon[:]:
            member_types = member.elemental_type.split('/')
            for e_type in member_types:
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

        for member in self.get_member_by_type("Pokemon"):
            for e_type in member.elemental_type.split("/"):
                if e_type in members:
                    members[e_type].append(member)
                else:
                    members[e_type] = [member]
        return members
        
    def get_member_by_id(self, id: str):
        """ Gets a single member from the party based on id.
        :param int id: The ID of the party member to be retrieved.
        :return: Returns the party member object (Pokemon or Egg) based on the given ID.
        :rtype: Pokemon or Egg
        """
        if id[0] == "p":
            result = [p for p in self.pokemon if p.id == id]
        elif id[0] == "e":
            result = [e for e in self.eggs if e.id == id]
        else:
            result = None
        
        if result:
            return result[0]

    def get_member_by_type(self, type: str) -> List:
        """ Gets a list of members from pc_storage and party based on indicated type
        :param str type: The type to filter by
        :return: List of members
        :rtype: List
        """
        if type == "Pokemon":
            return self.pokemon[:]
        elif type == "Egg":
            return self.eggs[:]
        
    def get_stats(self) -> PokeStats:
        """ Populates a stats object with statistics about the party manager
        :return: PokeStats object
        :rtype: PokeStats
        """
        members_by_type = self._total_per_elemental_type()
        total_eggs = len(self.get_member_by_type('Egg'))
        total_KO = 0
        total_steps = self.total_steps
        for member in self.all_members:
            if member.member_type == 'Pokemon' and member.is_KO:
                total_KO += 1
        return PokeStats(members_by_type, total_eggs, total_KO, total_steps, self.player_name)

    def _total_per_elemental_type(self) -> dict:
        """ Populates and returns a dictionary of total amount of members by each elemental type, eg:
            {'Grass': 5, 'Fire': 1}
        :return: Dictionary of totals
        :rtype: dict
        """
        members_by_type = self.get_all_members_by_elemental_type()
        print(members_by_type)
        return {k:len(v) for k,v in members_by_type.items()}

    def to_dict(self):
        dikt = {
            "player_name": self.player_name,
            "total_steps": self.total_steps,
            "id": self.id
        }
        return dikt