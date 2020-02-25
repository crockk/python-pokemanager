"""
Author: Tushya Iyer, Nolan Crooks
ACIT 2515
Date: 2/25/2020
"""

from party_manager import PartyManager
from egg import Egg
from pokemon import Pokemon
import unittest
import random
from datetime import datetime, date


class TestPartyManager(unittest.TestCase):

    def setUp(self) -> None:
        random.seed(13)
        self.party_manager = PartyManager('Nolan')

    def test_valid_init(self):
        self.assertIsInstance(self.party_manager, PartyManager)

    def test_invalid_init(self):
        with self.assertRaises(TypeError):
            manager = PartyManager(123)

    def test_create_member(self):
        with self.assertRaises(ValueError):
            self.party_manager.create_member('Pakemun', 5, 'Route 55')
        with self.assertRaises(ValueError):
            self.party_manager.create_member('Pokemon', '5', 'Route 55')

        self.party_manager.create_member('Pokemon', 5, 'Route 55')
        self.assertIsInstance(self.party_manager.get_member_by_id(1), Pokemon)

        self.party_manager.create_member('Egg', 5, 'Route 55')
        self.assertIsInstance(self.party_manager.get_member_by_id(2), Egg)

    def test_move_to_party(self):
        self.party_manager.create_member('Pokemon', 5, 'Route 55')
        self.party_manager.create_member('Pokemon', 5, 'Route 55')
        self.party_manager.create_member('Pokemon', 5, 'Route 55')
        self.party_manager.create_member('Pokemon', 5, 'Route 55')
        self.party_manager.create_member('Pokemon', 5, 'Route 55')
        self.party_manager.create_member('Pokemon', 5, 'Route 55')
        self.party_manager.create_member('Pokemon', 5, 'Route 55')

        self.assertTrue(self.party_manager.move_to_party(1))

        self.party_manager.move_to_party(2)
        self.party_manager.move_to_party(3)
        self.party_manager.move_to_party(4)
        self.party_manager.move_to_party(5)
        self.party_manager.move_to_party(6)

        self.assertFalse(self.party_manager.move_to_party(7))

    def test_move_to_pc(self):
        self.party_manager.create_member('Pokemon', 5, 'Route 55')
        self.party_manager.move_to_party(1)

        self.assertTrue(self.party_manager.move_to_pc(1))

        self.assertFalse(self.party_manager.move_to_pc(1))

    def test_release_party_member(self):
        self.party_manager.create_member('Pokemon', 5, 'Route 55')
        self.party_manager.move_to_party(1)

        self.assertTrue(self.party_manager.release_party_member(1))

        self.assertFalse(self.party_manager.release_party_member(1))

    def test_release_pc_pokemon(self):
        self.party_manager.create_member('Pokemon', 5, 'Route 55')
    
        self.assertTrue(self.party_manager.release_pc_pokemon(1))
    
        self.assertFalse(self.party_manager.release_pc_pokemon(1))

    # def test_get_members_by_elemental_type(self):
    #     self.party_manager.create_member('Pokemon', 5, 'Route 55')
    #     self.party_manager.create_member('Pokemon', 5, 'Route 55')
    #     self.party_manager.create_member('Pokemon', 5, 'Route 55')
    #     self.party_manager.create_member('Pokemon', 5, 'Route 55')
    #
    #     length = (self.party_manager.get_members_by_elemental_type(tuple('Grass')))
    #     print(length)
    #     self.assertEqual(length, 5)



