"""
Author: Tushya Iyer, Nolan Crooks
ACIT 2515
Date: 2/13/2020
"""

from peewee import CharField, IntegerField, DecimalField, DateField, BooleanField, ForeignKeyField
from abc import abstractmethod, ABC
from datetime import date, datetime
from random import uniform
from db import BaseModel
from typing import Dict
from pokedex import RandomStats


class PartyMember(BaseModel):
    """ Defines the abstract class PartyMember

    This class defines various base stats of the PartyMember that inherits it.

    CLASS VARIABLES
    _MIN_WEIGHT and _MAX_WEIGHT: Range defining the weight of the party member

    _MIN_HEIGHT and _MAX_HEIGHT: Range defining the height of the party member

    """

    # json: dict

    _MIN_WEIGHT = 50  # KG
    _MAX_WEIGHT = 1000  # KG

    _MIN_HEIGHT = 80  # CM
    _MAX_HEIGHT = 1500  # CM
    

    # def __init__(self, id: int, pokedex_num: int, source: str, nickname: str, item: str = None, json: Dict = None) -> None:
    #     """ Initalizes instance properties
    #
    #     :param int id: Unique identifier for pokemon
    #     :param int pokedex_num: Number corresponding with the pokedex entry of that member
    #     :param str source: The location that the member was acquired
    #     :param str nickname: A given nickname
    #     :param str item: The item that the member is holding
    #     :return: No return
    #     :rtype: None
    #
    #     """
    #     self._validate_int(id, 1, "ID must be an Integer greater than or equal to 1")
    #
    #     self._validate_int(pokedex_num, 1, "Pokedex Number must be greater than or equal to 1")
    #
    #     self._validate_string(source, "Source must be a none-blank String")
    #
    #     self._validate_string(nickname, "Nickname must be a none-blank String")
    #
    #     if item is not None:
    #         self._validate_string(item, "Item must be a none-blank String")
    #
    #     if json is not None:
    #         self._in_party = json['in_party']
    #         self._weight = json['weight']
    #         self._height = json['height']
    #         self._date_acquired = json['date_acquired']
    #     else:
    #         self._in_party = False
    #         self._weight = self._rand_weight()
    #         self._height = self._rand_height()
    #         self._date_acquired = datetime.now().date()
    #
    #     self._id = id
    #     self._pokedex_num = pokedex_num
    #     self._source = source
    #     self._nickname = nickname
    #     self._item = item

#     @property
#     def id(self) -> int:
#         """ Gets and returns ID

#         :return: ID
#         :rtype: Integer

#         """
#         return self._id

#     @property
#     def pokedex_num(self) -> int:
#         """ Gets and returns the pokedex number

#         :return: Pokedex number
#         :rtype: Integer

#         """
#         return self._pokedex_num

#     @property
#     def nickname(self) -> str:
#         """ Gets and returns

#         :return: Nickname
#         :rtype: String

#         """
#         return self._nickname

#     @nickname.setter
#     def nickname(self, new_nickname: str) -> None:
#         """ Sets a new nickname

#         :param str new_nickname: New nickname for member
#         :return: No return
#         :rtype: None

#         """
#         self._validate_string(new_nickname, "Nickname must be a none-blank String")

#         self._nickname = new_nickname

#     @property
#     def in_party(self) -> bool:
#         """ Gets and returns the in_party property

#         :return: in_party property
#         :rtype: Boolean

#         """
#         return self._in_party

#     @property
#     def weight(self) -> float:
#         """ Gets and returns weight property

#         :return: Weight property
#         :rtype: Float

#         """
#         return self._weight

#     @property
#     def height(self) -> float:
#         """ Gets and returns height property

#         :return: Height property
#         :rtype: Float

#         """
#         return self._height

#     @abstractmethod
#     def description(self) -> str:
#         """ Abstract method description implemented by child classes

#         :raise: NotImplementedError
#         :return: None
#         :rtype: None
#         """
#         raise NotImplementedError

#     @property
#     def source(self) -> str:
#         """ Gets and returns source property

#         :return: Source property
#         :rtype: String

#         """
#         return self._source

#     @property
#     def date_acquired(self) -> date:
#         """ Gets and returns date_acquired

#         :return: Returns the date acquired
#         :rtype: Date

#         """
#         return self._date_acquired

#     @property
#     def held_item(self) -> str:
#         """ Gets and returns held_item

#         :return: The member's held item
#         :rtype: String

#         """
#         if self._item:
#             return self._item
#         else:
#             return "None"

#     @held_item.setter
#     def held_item(self, item: str) -> None:
#         """ Set held_item property for the member

#         :param str item: The new held item
#         :return: No return
#         :rtype: None

#         """
#         self._validate_string(item, "Item must be a none-blank String")

#         self._item = item

#     @abstractmethod
#     def member_type(self) -> None:
#         """ Abstract method member_type implemented in child classes

#         :raise: NotImplementedError
#         :return: None
#         :rtype: None
#         """
#         raise NotImplementedError

#     @abstractmethod
#     def to_dict(self) -> None:
#         """ Abstract method to_dict implemented in child classes

#         :raise: NotImplementedError
#         :return: None
#         :rtype: None
#         """
#         raise NotImplementedError


    pokedex_num = IntegerField(column_name='pokedex_num')
    nickname = CharField(column_name='nickname')
    in_party = BooleanField(default=False)
    weight = DecimalField(column_name='weight', default=RandomStats.rand_weight)
    height = DecimalField(column_name='height', default=RandomStats.rand_height)
    source = CharField(column_name='source', null=True)
    date_acquired = DateField(default=datetime.now)
    item = CharField(column_name='item', null=True)