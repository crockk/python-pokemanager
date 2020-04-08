"""
Author: Tushya Iyer, Nolan Crooks
ACIT 2515
Date: 2/13/2020
"""

from peewee import CharField, IntegerField, DecimalField, DateField, BooleanField
from abc import abstractmethod
from datetime import datetime
from db.db import BaseModel
from pokemodule.pokedex import Pokedex, RandomStats


class PartyMember(BaseModel):
    """ Defines the abstract class PartyMember

    This class defines various base stats of the PartyMember that inherits it.

    CLASS VARIABLES
    _MIN_WEIGHT and _MAX_WEIGHT: Range defining the weight of the party member

    _MIN_HEIGHT and _MAX_HEIGHT: Range defining the height of the party member

    """

    @property
    def elemental_type(self):
        return Pokedex[self.pokedex_num][1]

    @property
    def species(self):
        return Pokedex[self.pokedex_num][0]

    @abstractmethod
    def to_dict(self) -> None:
        """ Abstract method to_dict implemented in child classes

        :raise: NotImplementedError
        :return: None
        :rtype: None
        """
        raise NotImplementedError

    pokedex_num = IntegerField(column_name='pokedex_num')
    nickname = CharField(column_name='nickname', null=True)
    in_party = BooleanField(default=False)
    weight = DecimalField(column_name='weight', default=RandomStats.rand_weight)
    height = DecimalField(column_name='height', default=RandomStats.rand_height)
    source = CharField(column_name='source', null=True)
    date_acquired = DateField(default=datetime.now)
    item = CharField(column_name='item', null=True)
