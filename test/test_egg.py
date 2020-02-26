"""
Author: Tushya Iyer, Nolan Crooks
ACIT 2515
Date: 2/25/2020
"""

from egg import Egg
import unittest
import random
from datetime import datetime, date

class EggTestClass(unittest.TestCase):

    _ID = 1

    def setUp(self):
        random.seed(13)
        self.egg = Egg(self._ID, 7, "Calgary", nickname="Flyboy")
        # print(self.egg.steps_remaining, self.egg.steps_required)

    def test_constructor(self):
        self.assertIsInstance(self.egg, Egg)

        with self.assertRaises(ValueError):
            e = Egg(self._ID, -1, "Calgary")
        
        with self.assertRaises(TypeError):
            e = Egg(self._ID, 6, 2)

    def test_steps_required(self):
        self.assertEqual(self.egg.steps_required, 3801)
        self.egg.add_steps(1)
        self.assertEqual(self.egg.steps_required, 3801)

    def test_steps_remaining(self):
        self.assertEqual(self.egg.steps_remaining, 3801)
        self.egg.add_steps(1)
        self.assertEqual(self.egg.steps_remaining, 3800)

    def test_add_steps(self):
        steps_remaining = self.egg.steps_remaining
        self.egg.add_steps(10)
        self.assertEqual(self.egg.steps_remaining, steps_remaining - 10)

        self.egg.add_steps(steps_remaining)
        self.assertTrue(self.egg.hatched)

    def test_description(self):
        print(self.egg.height, self.egg._weight)
        self.assertEqual(self.egg.description, "Your Flyboy is 1053.07cm tall and 296.06kg. Not currently in party" )

    def test_hatched(self):
        self.egg.add_steps(self.egg.steps_remaining)
        self.assertTrue(self.egg.hatched)

    def test_member_type(self):
        self.assertEqual(self.egg.member_type(), "Egg")
