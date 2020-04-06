"""
Author: Tushya Iyer, Nolan Crooks
ACIT 2515
Date: 2/24/2020
"""

from pokemodule.pokemon import Pokemon
import unittest
import random
from datetime import datetime


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
        self.assertLessEqual(self.pokemon.weight, 1000)
        
    def test_height(self):

        # 80 and 1500 come from private class variables in PartyMember class
        self.assertGreaterEqual(self.pokemon.height, 80)
        self.assertLessEqual(self.pokemon.height, 1500)

    def test_source(self):
        self.assertEqual(self.pokemon.source, "BC")

    def test_date_acquired(self):
        self.assertEqual(self.pokemon.date_acquired, datetime.now().date())

    def test_held_item(self):

        self.assertEqual(self.pokemon.held_item, "None")
        self.pokemon.held_item = "Wings of Bud"
        self.assertEqual(self.pokemon.held_item, "Wings of Bud")

    def test_moves(self):
        self.assertEqual(len(self.pokemon.moves), 4)
    
    def test_xp_till_next_level(self):
        # 80 and 120 come from private class variables in Pokemon class
        self.assertGreaterEqual(self.pokemon.xp_till_next_level, 80)
        self.assertLessEqual(self.pokemon.xp_till_next_level, 120)

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
        self.assertLessEqual(self.pokemon.attack, 18)

    def test_defense(self):
        # 3 and 18 come from private class variables in Pokemon class
        self.assertGreaterEqual(self.pokemon.defense, 3)
        self.assertLessEqual(self.pokemon.defense, 18)

    def test_speed(self):
        # 3 and 18 come from private class variables in Pokemon class
        self.assertGreaterEqual(self.pokemon.speed, 3)
        self.assertLessEqual(self.pokemon.speed, 18)

    def test_total_hp(self):
        # 5 and 35 come from private class variables in Pokemon class
        self.assertGreaterEqual(self.pokemon.total_hp, 15)
        print(self.pokemon.total_hp, 'HP')
        self.assertLessEqual(self.pokemon.total_hp, 35)

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
        self.assertEqual(self.pokemon.use_move(1), "Flyboy used Growl!! it did 0 damage!")
        with self.assertRaises(ValueError):
            self.pokemon.use_move(5)

        with self.assertRaises(ValueError):
            self.pokemon.use_move(-1)

    def test_display_moves(self):
        # self.assertEqual()  
        self.maxDiff = None
        expected_str = "\nMove Index    |Move Name     |Damage        \n============================================\n1             |Growl         |0             \n2             |Tail Whip     |0             \n3             |Splash        |0             \n4             |Leer          |0             \n"
        self.assertEqual(self.pokemon.display_moves(), expected_str)

        expected_str = "\nMove Index    |Move Name     |Damage        \n============================================\n1             |Growl         |0             \n"
        self.assertEqual(self.pokemon.display_moves(1), expected_str)

        with self.assertRaises(ValueError):
            self.pokemon.display_moves(-1)

        with self.assertRaises(ValueError):
            self.pokemon.display_moves(5)

    def test_add_xp(self):
        # 3 and 18 come from private class variables in Pokemon class
        self.assertGreaterEqual(self.pokemon.xp_till_next_level, 80)
        self.assertLessEqual(self.pokemon.xp_till_next_level, 120)

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

    def test_to_dict(self):
        poke_dict = self.pokemon.to_dict()

        test_dict = {
            "id": self.pokemon.id,
            "member_type": self.pokemon.member_type(),
            "pokedex_num": self.pokemon.pokedex_num,
            "source": self.pokemon.source,
            "nickname": self.pokemon.nickname,
            "item": None,

            "in_party": self.pokemon.in_party,
            "weight": self.pokemon.weight,
            "height": self.pokemon.height,
            "date_acquired": str(self.pokemon.date_acquired),

            "ability": self.pokemon.ability,
            "elemental_type": self.pokemon.elemental_type,
            "next_level_xp": self.pokemon._next_level_xp,
            "current_level_xp": self.pokemon._current_level_xp,
            "level": self.pokemon.level,
            "attack": self.pokemon.attack,
            "speed": self.pokemon.speed,
            "total_hp": self.pokemon.total_hp,
            "current_hp": self.pokemon.current_hp,
            "is_KO": self.pokemon.is_KO,
            "moves": self.pokemon.moves
        }

        self.assertEqual(poke_dict, test_dict)
