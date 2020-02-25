"""
Author: Tushya Iyer, Nolan Crooks
ACIT 2515
Date: 2/24/2020
"""

from pokemon import Pokemon
import unittest

class PokemonTestClass(unittest.TestCase):

    def set_up(self):
        self._pokemon = Pokemon('Pokemon', 10, "BC", "Flyboy", "Wings of Bud", "wings")



