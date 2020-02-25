"""
Author: Tushya Iyer, Nolan Crooks
ACIT 2515
Date: 2/24/2020
"""

from pokemon import Pokemon
import unittest
import random
from datetime import datetime, date

class PokemonTestClass(unittest.TestCase):

    _ID = 1

    def setUp(self):
        random.seed(13)
        self.pokemon = Pokemon(self._ID, 10, "BC", "Flyboy", ability="wings")
    

    def test_constructor(self):
        self.assertIsInstance(self.pokemon, Pokemon)

        with self.assertRaises(TypeError):
            p = Pokemon("hi", 10, "BC", "Flyboy", "Wings of Bud", "wings")

        with self.assertRaises(ValueError):
            p = Pokemon(0, 10, "BC", "Flyboy", "Wings of Bud", "wings")

        with self.assertRaises(TypeError):
            p = Pokemon(self._ID, 10, 0, "Flyboy", "Wings of Bud", "wings")

        with self.assertRaises(ValueError):
            p = Pokemon(0, 10, "", "", item="Wings of Bud")

    def test_id(self):
        self.assertEqual(self.pokemon.id, self._ID)

    def test_pokedex_num(self):
        self.assertEqual(self.pokemon.pokedex_num, 10)

    def test_nickname(self):
        self.assertEqual(self.pokemon.nickname, "Flyboy")

        with self.assertRaises(ValueError):
            self.pokemon.nickname = ''

        self.pokemon.nickname = 'bob-jim'

        self.assertEqual(self.pokemon.nickname, 'bob-jim')

    def test_in_party(self):
        self.assertFalse(self.pokemon.in_party)

    def test_weight(self):

        # 50 and 1000 come from private class variables in PartyMember class
        self.assertGreaterEqual(self.pokemon.weight, 50)
        self.assertLess(self.pokemon.weight, 1000)
        
    def test_height(self):

        # 80 and 1500 come from private class variables in PartyMember class
        self.assertGreaterEqual(self.pokemon.height, 80)
        self.assertLess(self.pokemon.height, 1500)

    def test_source(self):
        self.assertEqual(self.pokemon.source, "BC")

    def test_date_acquired(self):
        self.assertEqual(self.pokemon.date_acquired, datetime.now().date())

    def test_held_item(self):

        self.assertEqual(self.pokemon.held_item, "None")
        self.pokemon.held_item = "Wings of Bud"
        self.assertEqual(self.pokemon.held_item, "Wings of Bud")

    def test_moves(self):
        pass
    
    def test_xp_till_next_level(self):
        # 80 and 120 come from private class variables in Pokemon class
        self.assertGreaterEqual(self.pokemon.xp_till_next_level, 80)
        self.assertLess(self.pokemon.xp_till_next_level, 120)

    def test_level(self):
        self.assertEqual(self.pokemon.level, 5)

        self.pokemon.add_xp(self.pokemon.xp_till_next_level)

        self.assertEqual(self.pokemon.level, 6)

    def test_ability(self):
        self.assertEqual(self.pokemon.ability, "wings")
        p = Pokemon(self._ID, 10, "BC", "Flyboy")

        self.assertEqual(p.ability, 'None')

    def test_elemental_type(self):
        self.assertTupleEqual(self.pokemon.elemental_type, ("Flying", "Dragon"))
        p = Pokemon(self._ID, 9, "BC", "Flyboy")

        self.assertTupleEqual(p.elemental_type, ("Ground",))

    def test_attack(self):
        # 3 and 18 come from private class variables in Pokemon class
        self.assertGreaterEqual(self.pokemon.attack, 3)
        self.assertLess(self.pokemon.attack, 18)

    def test_defense(self):
        # 3 and 18 come from private class variables in Pokemon class
        self.assertGreaterEqual(self.pokemon.defense, 3)
        self.assertLess(self.pokemon.defense, 18)

    def test_speed(self):
        # 3 and 18 come from private class variables in Pokemon class
        self.assertGreaterEqual(self.pokemon.speed, 3)
        self.assertLess(self.pokemon.speed, 18)

    def test_total_hp(self):
        # 5 and 35 come from private class variables in Pokemon class
        self.assertGreaterEqual(self.pokemon.total_hp, 15)
        self.assertLess(self.pokemon.total_hp, 35)

    def test_current_hp(self):
        # 35 comes from private class variables in Pokemon class
        self.assertLessEqual(self.pokemon.current_hp, 35)

    def test_KO(self):
        self.assertFalse(self.pokemon.is_KO)

        self.pokemon.damage(self.pokemon.current_hp)

        self.assertTrue(self.pokemon.is_KO)
    
    def test_description(self):
        self.assertEqual(self.pokemon.description, f"Your {self.pokemon.nickname} is {self.pokemon.height}cm tall and {self.pokemon.weight}kg. \n " \
               f"Current level: {self.pokemon.level}, exp to next level: {self.pokemon.xp_till_next_level}. \n" \
               f"Not currently in party")

    def test_use_move(self):
        pass

    def test_add_xp(self):
        # 3 and 18 come from private class variables in Pokemon class
        self.assertGreaterEqual(self.pokemon.xp_till_next_level, 80)
        self.assertLess(self.pokemon.xp_till_next_level, 120)

        self.assertEqual(self.pokemon.level, 5)

        self.pokemon.add_xp(self.pokemon.xp_till_next_level + 1)

        self.assertEqual(self.pokemon.level, 6)

    def test_heal(self):
        self.assertEqual(self.pokemon.current_hp, self.pokemon.total_hp)

        with self.assertRaises(TypeError):
            self.pokemon.heal("eee")

        
        self.pokemon.heal(1)

        self.pokemon.damage(10)

        self.pokemon.heal(5)

    def test_member_type(self):
        self.assertEqual(self.pokemon.member_type(), "Pokemon")