"""
Author: Tushya Iyer, Nolan Crooks
ACIT 2515
Date: 2/25/2020
"""

from pokemodule.party_manager import PartyManager
from pokemodule.egg import Egg
from pokemodule.pokemon import Pokemon
from unittest import TestCase
import random
import os
import sqlite3
from create_tables import create_tables
from drop_tables import drop_tables


class TestPartyManager(TestCase):

    def setUp(self) -> None:
        create_tables()
        random.seed(13)

        self.party_manager = PartyManager(player_name = 'Nolan')
        self.party_manager.save()

    def tearDown(self):
        drop_tables()

    def test_valid_init(self):
        self.assertIsInstance(self.party_manager, PartyManager)

        self.assertEqual(self.party_manager.player_name, 'Nolan')

    def test_create_member(self):
        self.assertEqual(len(Pokemon.select()[:]), 0)
        p1 = Pokemon.create(nickname = 'Pakemun', id=1, pokedex_num=4, player=self.party_manager)
        p1.save()
        self.assertEqual(len(Pokemon.select()[:]), 1)        

    def test_move_to_party(self):
        p1 = Pokemon.create(id=self.party_manager._ID_MANAGER.pokemon_id(), pokedex_num=4, player=self.party_manager)
        p1.save()
        p2 = Pokemon.create(id=self.party_manager._ID_MANAGER.pokemon_id(), pokedex_num=4, player=self.party_manager)
        p2.save()
        p3 = Pokemon.create(id=self.party_manager._ID_MANAGER.pokemon_id(), pokedex_num=4, player=self.party_manager)
        p3.save()
        p4 = Pokemon.create(id=self.party_manager._ID_MANAGER.pokemon_id(), pokedex_num=4, player=self.party_manager)
        p4.save()
        p5 = Pokemon.create(id=self.party_manager._ID_MANAGER.pokemon_id(), pokedex_num=4, player=self.party_manager)
        p5.save()
        p6 = Pokemon.create(id=self.party_manager._ID_MANAGER.pokemon_id(), pokedex_num=4, player=self.party_manager)
        p6.save()
        p7 = Pokemon.create(id=self.party_manager._ID_MANAGER.pokemon_id(), pokedex_num=4, player=self.party_manager)
        p7.save()

        self.assertTrue(self.party_manager.move_to_party(p1.id))

        self.party_manager.move_to_party(p2.id)
        self.party_manager.move_to_party(p3.id)
        self.party_manager.move_to_party(p4.id)
        self.assertFalse(self.party_manager.move_to_party(p4.id))

        self.assertFalse(self.party_manager.move_to_party(self.party_manager._ID_MANAGER.pokemon_id()))

        self.party_manager.move_to_party(p5.id)
        self.party_manager.move_to_party(p6.id)

        self.assertFalse(self.party_manager.move_to_party(p7.id))


    def test_move_to_pc(self):

        p1 = Pokemon.create(id=self.party_manager._ID_MANAGER.pokemon_id(), pokedex_num=4, player=self.party_manager)
        p1.save()

        self.party_manager.move_to_party(p1.id)

        self.assertTrue(self.party_manager.move_to_pc(p1.id))

        self.assertFalse(self.party_manager.move_to_pc(p1.id))

    def test_release_member(self):
        p1 = Pokemon.create(id=self.party_manager._ID_MANAGER.pokemon_id(), pokedex_num=4, player=self.party_manager)
        p1.save()
        self.party_manager.move_to_party(p1.id)

        self.assertTrue(self.party_manager.release_member(p1.id))

        self.assertFalse(self.party_manager.release_member(p1.id))

        p2 = Pokemon.create(id=self.party_manager._ID_MANAGER.pokemon_id(), pokedex_num=4, player=self.party_manager)
        p2.save()
    
        self.assertTrue(self.party_manager.release_member(p2.id))

        self.assertFalse(self.party_manager.release_member(p2.id))

    def test_get_members_by_elemental_type(self):

        p1 = Pokemon.create(id=self.party_manager._ID_MANAGER.pokemon_id(), pokedex_num=5, player=self.party_manager)
        p1.save()
        p1 = Pokemon.create(id=self.party_manager._ID_MANAGER.pokemon_id(), pokedex_num=5, player=self.party_manager)
        p1.save()
        p1 = Pokemon.create(id=self.party_manager._ID_MANAGER.pokemon_id(), pokedex_num=5, player=self.party_manager)
        p1.save()
        p1 = Pokemon.create(id=self.party_manager._ID_MANAGER.pokemon_id(), pokedex_num=5, player=self.party_manager)
        p1.save()

        members = self.party_manager.get_members_by_elemental_type(('Grass', ))
        self.assertEqual(len(members['Grass']), 4)

        p1 = Pokemon.create(id=self.party_manager._ID_MANAGER.pokemon_id(), pokedex_num=10, player=self.party_manager)
        p1.save()
        p1 = Pokemon.create(id=self.party_manager._ID_MANAGER.pokemon_id(), pokedex_num=10, player=self.party_manager)
        p1.save()
        p1 = Pokemon.create(id=self.party_manager._ID_MANAGER.pokemon_id(), pokedex_num=5, player=self.party_manager)
        p1.save()
        p1 = Pokemon.create(id=self.party_manager._ID_MANAGER.pokemon_id(), pokedex_num=5, player=self.party_manager)
        p1.save()

        grass = self.party_manager.get_members_by_elemental_type(('Grass', ))
        dragon = self.party_manager.get_members_by_elemental_type(('Dragon', ))

        self.assertEqual(len(grass['Grass']), 6)
        self.assertEqual(len(dragon['Dragon']), 2)


    def test_get_member_by_id(self):
        p1 = Pokemon.create(id=self.party_manager._ID_MANAGER.pokemon_id(), pokedex_num=4, player=self.party_manager)
        p1.save()

        self.assertIsInstance(self.party_manager.get_member_by_id(p1.id), Pokemon)

        self.assertIsNone(self.party_manager.get_member_by_id('p9999'))

        self.party_manager.move_to_party(p1.id)

        self.assertIsInstance(self.party_manager.get_member_by_id(p1.id), Pokemon)


    def test_get_all_party_members(self):
        p1 = Pokemon.create(id=self.party_manager._ID_MANAGER.pokemon_id(), pokedex_num=4, player=self.party_manager)
        p1.save()
        p2 = Pokemon.create(id=self.party_manager._ID_MANAGER.pokemon_id(), pokedex_num=4, player=self.party_manager)
        p2.save()
        p3 = Pokemon.create(id=self.party_manager._ID_MANAGER.pokemon_id(), pokedex_num=4, player=self.party_manager)
        p3.save()
        p4 = Pokemon.create(id=self.party_manager._ID_MANAGER.pokemon_id(), pokedex_num=4, player=self.party_manager)
        p4.save()
        p5 = Pokemon.create(id=self.party_manager._ID_MANAGER.pokemon_id(), pokedex_num=4, player=self.party_manager)
        p5.save()
        p6 = Pokemon.create(id=self.party_manager._ID_MANAGER.pokemon_id(), pokedex_num=4, player=self.party_manager)
        p6.save()

        self.party_manager.move_to_party(p1.id)
        self.party_manager.move_to_party(p2.id)
        self.party_manager.move_to_party(p3.id)
        self.party_manager.move_to_party(p4.id)
        self.party_manager.move_to_party(p5.id)
        self.party_manager.move_to_party(p6.id)

        self.assertEqual(len(self.party_manager.party_members), 6)

    def test_get_all_pc_members(self):
        p1 = Pokemon.create(id=self.party_manager._ID_MANAGER.pokemon_id(), pokedex_num=4, player=self.party_manager)
        p1.save()
        p2 = Pokemon.create(id=self.party_manager._ID_MANAGER.pokemon_id(), pokedex_num=4, player=self.party_manager)
        p2.save()
        p3 = Pokemon.create(id=self.party_manager._ID_MANAGER.pokemon_id(), pokedex_num=4, player=self.party_manager)
        p3.save()
        p4 = Pokemon.create(id=self.party_manager._ID_MANAGER.pokemon_id(), pokedex_num=4, player=self.party_manager)
        p4.save()
        p5 = Pokemon.create(id=self.party_manager._ID_MANAGER.pokemon_id(), pokedex_num=4, player=self.party_manager)
        p5.save()
        p6 = Pokemon.create(id=self.party_manager._ID_MANAGER.pokemon_id(), pokedex_num=4, player=self.party_manager)
        p6.save()

        self.assertEqual(len(self.party_manager.pc_members), 6)

    def test_get_all_members(self):
        p1 = Pokemon.create(id=self.party_manager._ID_MANAGER.pokemon_id(), pokedex_num=4, player=self.party_manager)
        p1.save()
        p2 = Pokemon.create(id=self.party_manager._ID_MANAGER.pokemon_id(), pokedex_num=4, player=self.party_manager)
        p2.save()
        p3 = Pokemon.create(id=self.party_manager._ID_MANAGER.pokemon_id(), pokedex_num=4, player=self.party_manager)
        p3.save()
        p4 = Pokemon.create(id=self.party_manager._ID_MANAGER.pokemon_id(), pokedex_num=4, player=self.party_manager)
        p4.save()
        p5 = Pokemon.create(id=self.party_manager._ID_MANAGER.pokemon_id(), pokedex_num=4, player=self.party_manager)
        p5.save()
        p6 = Pokemon.create(id=self.party_manager._ID_MANAGER.pokemon_id(), pokedex_num=4, player=self.party_manager)
        p6.save()

        self.party_manager.move_to_party(p1.id)
        self.party_manager.move_to_party(p3.id)
        self.party_manager.move_to_party(p5.id)

        self.assertEqual(len(self.party_manager.all_members), 6)

    def test_get_member_by_type(self):
        p1 = Pokemon.create(id=self.party_manager._ID_MANAGER.pokemon_id(), pokedex_num=4, player=self.party_manager)
        p1.save()
        
        e1 = Egg.create(id=self.party_manager._ID_MANAGER.egg_id(), pokedex_num=4, player=self.party_manager)
        e1.save()

        members = self.party_manager.get_member_by_type('Pokemon')

        self.assertEqual(len(members), 1)

    def test_walk(self):
        e1 = Egg.create(id=self.party_manager._ID_MANAGER.egg_id(), pokedex_num=4, player=self.party_manager)
        e1.save()
        e2 = Egg.create(id=self.party_manager._ID_MANAGER.egg_id(), pokedex_num=4, player=self.party_manager)
        e2.save()
        e3 = Egg.create(id=self.party_manager._ID_MANAGER.egg_id(), pokedex_num=4, player=self.party_manager)
        e3.save()
        

        self.party_manager.move_to_party(e1.id)
        self.party_manager.move_to_party(e2.id)
        self.party_manager.move_to_party(e3.id)

        # Mazimum number of steps required to hatch is 5000, therefor all egs should hatch
        # For each hatched egg there is 3 calls to _write_to_file
        self.party_manager.walk(5000)

        stats = self.party_manager.get_stats()

        self.assertEqual(stats.get_total_steps(), 5000)


    def test_add_xp(self):

        p1 = Pokemon.create(id=self.party_manager._ID_MANAGER.pokemon_id(), pokedex_num=4, player=self.party_manager)
        p1.save()

        xp_to_add = p1.xp_till_next_level - 1
        self.party_manager.add_xp_to_pokemon(p1.id, xp_to_add)

        self.assertEqual(self.party_manager.get_member_by_id(p1.id).xp_till_next_level, 1)

    def test_get_stats(self):
        e1 = Egg.create(id=self.party_manager._ID_MANAGER.egg_id(), pokedex_num=4, player=self.party_manager)
        e1.save()
        p1 = Pokemon.create(id=self.party_manager._ID_MANAGER.pokemon_id(), pokedex_num=5, player=self.party_manager)
        p1.save()
        p2 = Pokemon.create(id=self.party_manager._ID_MANAGER.pokemon_id(), pokedex_num=1, player=self.party_manager)
        p2.save()

        self.party_manager.move_to_party(e1.id)
        self.party_manager.move_to_party(p1.id)
        self.party_manager.move_to_party(p2.id)

        poke1 = p1
        poke2 = p2

        poke1.damage(poke1.total_hp)
        poke2.damage(poke2.total_hp)

        stats = self.party_manager.get_stats()

        self.assertEqual(stats.get_total_KO(), 2)

        self.assertEqual(stats.get_total_steps(), 0)

        self.assertEqual(len(stats.get_total_by_type()), 1)

        self.assertEqual(stats.get_total_eggs(), 1)

        stat_check = {
            'player_name': 'Nolan',
            'total_by_type': {'Grass': 2}, 
            'total_eggs': 1, 
            'total_KO': 2, 
            'total_steps': 0
        }
        self.assertDictEqual(stats.to_dict(), stat_check)
