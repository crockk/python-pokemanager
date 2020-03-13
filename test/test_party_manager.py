"""
Author: Tushya Iyer, Nolan Crooks
ACIT 2515
Date: 2/25/2020
"""

from party_manager import PartyManager
from egg import Egg
from pokemon import Pokemon
from unittest import TestCase, mock
import random
from datetime import datetime, date
import os


class TestPartyManager(TestCase):

    _FILEPATH = os.path.join("data", "pokedata.json")

    @mock.patch('party_manager.PartyManager._read_from_file', side_effect = FileNotFoundError)
    def setUp(self, mock_read_func) -> None:
        random.seed(13)

        self.party_manager = PartyManager('Nolan')
        self.mock_save_func = mock.Mock()
        self.party_manager._write_to_file = self.mock_save_func

    def test_valid_init(self):
        self.assertIsInstance(self.party_manager, PartyManager)

        self.assertEqual(self.party_manager._filepath, self._FILEPATH)

    def test_invalid_init(self):
        with self.assertRaises(TypeError):
            manager = PartyManager(123)

        with self.assertRaises(ValueError):
            manager = PartyManager('')

    def test_create_member(self):
        with self.assertRaises(ValueError):
            self.party_manager.create_member('Pakemun', 5, 'Route 55')
        with self.assertRaises(ValueError):
            self.party_manager.create_member('Pokemon', '5', 'Route 55')

        self.party_manager.create_member('Pokemon', 5, 'Route 55')
        self.assertIsInstance(self.party_manager.get_member_by_id(1), Pokemon)

        self.party_manager.create_member('Egg', 5, 'Route 55')
        self.assertIsInstance(self.party_manager.get_member_by_id(2), Egg)
        self.assertTrue(self.mock_save_func.called)
        self.assertEqual(self.mock_save_func.call_count, 2)

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
        self.assertFalse(self.party_manager.move_to_party(4))

        self.assertFalse(self.party_manager.move_to_party(9))

        self.party_manager.move_to_party(5)
        self.party_manager.move_to_party(6)

        self.assertFalse(self.party_manager.move_to_party(7))

        self.assertTrue(self.mock_save_func.called)
        self.assertEqual(self.mock_save_func.call_count, 19)

    def test_move_to_pc(self):
        self.party_manager.create_member('Pokemon', 5, 'Route 55')
        self.party_manager.move_to_party(1)

        self.assertTrue(self.party_manager.move_to_pc(1))

        self.assertFalse(self.party_manager.move_to_pc(1))

        self.assertTrue(self.mock_save_func.called)
        self.assertEqual(self.mock_save_func.call_count, 4)

    def test_release_party_member(self):
        self.party_manager.create_member('Pokemon', 5, 'Route 55')
        self.party_manager.move_to_party(1)

        self.assertTrue(self.party_manager.release_party_member(1))

        self.assertFalse(self.party_manager.release_party_member(1))

        self.assertTrue(self.mock_save_func.called)
        self.assertEqual(self.mock_save_func.call_count, 4)

    def test_release_pc_pokemon(self):
        self.party_manager.create_member('Pokemon', 5, 'Route 55')

        self.assertTrue(self.party_manager.release_pc_pokemon(1))

        self.assertFalse(self.party_manager.release_pc_pokemon(1))

        self.assertTrue(self.mock_save_func.called)
        self.assertEqual(self.mock_save_func.call_count, 2)

    def test_get_members_by_elemental_type(self):
        self.party_manager.create_member('Pokemon', 5, 'Route 55')
        self.party_manager.create_member('Pokemon', 5, 'Route 55')
        self.party_manager.create_member('Pokemon', 5, 'Route 55')
        self.party_manager.create_member('Pokemon', 5, 'Route 55')

        members = self.party_manager.get_members_by_elemental_type(('Grass', ))
        self.assertEqual(len(members['Grass']), 4)

        self.party_manager.create_member('Pokemon', 10, 'Route 55')
        self.party_manager.create_member('Pokemon', 10, 'Route 55')
        self.party_manager.create_member('Pokemon', 5, 'Route 55')
        self.party_manager.create_member('Pokemon', 5, 'Route 55')

        grass = self.party_manager.get_members_by_elemental_type(('Grass', ))
        dragon = self.party_manager.get_members_by_elemental_type(('Dragon', ))

        self.assertEqual(len(grass['Grass']), 6)
        self.assertEqual(len(dragon['Dragon']), 2)

        self.assertTrue(self.mock_save_func.called)
        self.assertEqual(self.mock_save_func.call_count, 8)

    def test_get_member_by_id(self):
        self.party_manager.create_member('Pokemon', 5, 'Route 55')

        self.assertIsInstance(self.party_manager.get_member_by_id(1), Pokemon)

        self.assertIsNone(self.party_manager.get_member_by_id(10))

        self.party_manager.move_to_party(1)

        self.assertIsInstance(self.party_manager.get_member_by_id(1), Pokemon)

        self.assertTrue(self.mock_save_func.called)
        self.assertEqual(self.mock_save_func.call_count, 3)

    def test_get_all_party_members(self):
        self.party_manager.create_member('Pokemon', 5, 'Route 55')
        self.party_manager.create_member('Pokemon', 5, 'Route 55')
        self.party_manager.create_member('Pokemon', 5, 'Route 55')
        self.party_manager.create_member('Pokemon', 5, 'Route 55')
        self.party_manager.create_member('Pokemon', 5, 'Route 55')
        self.party_manager.create_member('Pokemon', 5, 'Route 55')

        self.party_manager.move_to_party(1)
        self.party_manager.move_to_party(2)
        self.party_manager.move_to_party(3)
        self.party_manager.move_to_party(4)
        self.party_manager.move_to_party(5)
        self.party_manager.move_to_party(6)

        self.assertEqual(len(self.party_manager.get_all_party_members), 6)

        self.assertTrue(self.mock_save_func.called)
        self.assertEqual(self.mock_save_func.call_count, 18)

    def test_get_all_pc_members(self):
        self.party_manager.create_member('Pokemon', 5, 'Route 55')
        self.party_manager.create_member('Pokemon', 5, 'Route 55')
        self.party_manager.create_member('Pokemon', 5, 'Route 55')
        self.party_manager.create_member('Pokemon', 5, 'Route 55')
        self.party_manager.create_member('Pokemon', 5, 'Route 55')
        self.party_manager.create_member('Pokemon', 5, 'Route 55')

        self.assertEqual(len(self.party_manager.get_all_pc_members), 6)

        self.assertTrue(self.mock_save_func.called)
        self.assertEqual(self.mock_save_func.call_count, 6)

    def test_get_all_members(self):
        self.party_manager.create_member('Pokemon', 5, 'Route 55')
        self.party_manager.create_member('Pokemon', 5, 'Route 55')
        self.party_manager.create_member('Pokemon', 5, 'Route 55')
        self.party_manager.create_member('Pokemon', 5, 'Route 55')
        self.party_manager.create_member('Pokemon', 5, 'Route 55')
        self.party_manager.create_member('Pokemon', 5, 'Route 55')

        self.party_manager.move_to_party(1)
        self.party_manager.move_to_party(2)
        self.party_manager.move_to_party(3)

        self.assertEqual(len(self.party_manager.get_all_members), 6)

        self.assertTrue(self.mock_save_func.called)
        self.assertEqual(self.mock_save_func.call_count, 12)

    def test_get_member_by_type(self):
        self.party_manager.create_member('Pokemon', 5, 'Route 55')
        self.party_manager.create_member('Egg', 4, 'Route 55')

        members = self.party_manager.get_member_by_type('Pokemon')

        self.assertEqual(len(members), 1)

        self.assertTrue(self.mock_save_func.called)
        self.assertEqual(self.mock_save_func.call_count, 2)

    def test_walk(self):
        self.party_manager.create_member('Egg', 4, 'Route 55')
        self.party_manager.create_member('Egg', 5, 'Route 55')
        self.party_manager.create_member('Egg', 1, 'Route 55')

        self.party_manager.move_to_party(1)
        self.party_manager.move_to_party(2)
        self.party_manager.move_to_party(3)

        # Mazimum number of steps required to hatch is 5000, therefor all egs should hatch
        # For each hatched egg there is 3 calls to _write_to_file
        self.party_manager.walk(5000)

        stats = self.party_manager.get_stats()

        self.assertEqual(stats.get_total_steps(), 5000)

        self.assertTrue(self.mock_save_func.called)
        self.assertEqual(self.mock_save_func.call_count, 22)

    def test_add_xp(self):
        self.party_manager.create_member('Pokemon', 4, 'Route 55')
        xp_to_add = self.party_manager.get_member_by_id(1).xp_till_next_level - 1
        self.party_manager.add_xp_to_pokemon(1, xp_to_add)

        self.assertEqual(self.party_manager.get_member_by_id(1).xp_till_next_level, 1)

        self.assertTrue(self.mock_save_func.called)
        self.assertEqual(self.mock_save_func.call_count, 2)

    def test_get_stats(self):
        self.party_manager.create_member('Egg', 4, 'Route 55')
        self.party_manager.create_member('Pokemon', 5, 'Route 55')
        self.party_manager.create_member('Pokemon', 1, 'Route 55')

        self.party_manager.move_to_party(1)
        self.party_manager.move_to_party(2)
        self.party_manager.move_to_party(3)

        poke1 = self.party_manager.get_member_by_id(2)
        poke2 = self.party_manager.get_member_by_id(3)

        poke1.damage(poke1.total_hp)
        poke2.damage(poke2.total_hp)

        stats = self.party_manager.get_stats()

        self.assertEqual(stats.get_total_KO(), 2)

        self.assertEqual(stats.get_total_steps(), 0)

        self.assertEqual(len(stats.get_total_by_type()), 1)

        self.assertEqual(stats.get_total_eggs(), 1)

        self.assertTrue(self.mock_save_func.called)
        self.assertEqual(self.mock_save_func.call_count, 9)

        stat_check = {
            'total_by_type': {'Grass': 2}, 
            'total_eggs': 1, 
            'total_KO': 2, 
            'total_steps': 0
        }
        self.assertDictEqual(stats.to_dict(), stat_check)

    def test_read_from_file(self):
        self.party_manager = PartyManager("Yuto")
        self.party_manager.create_member('Egg', 4, 'Route 55')
        self.party_manager.create_member('Pokemon', 4, 'Route 55')
        self.party_manager.move_to_party(1)
        self.party_manager = PartyManager("Bluto")
        
        self.assertEqual(len(self.party_manager.get_all_members),2)

        os.remove(self._FILEPATH)

        self.party_manager = PartyManager("Yuto")

        

        