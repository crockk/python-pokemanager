"""
Author: Tushya Iyer, Nolan Crooks
ACIT 2515
Date: 2/17/2020
"""

from peewee import IntegerField, BooleanField, ForeignKeyField, CharField
from pokemodule.party_member import PartyMember
from pokemodule.pokemon import Pokemon
from pokemodule.party_manager import PartyManager
from pokemodule.pokedex import RandomStats, Pokedex


class Egg(PartyMember):
    """ Defines the subclass Egg which is a child of PartyMember

    This class is relatively simple, only adding a few new properties to the abstract
    class PartyMember it inherits from.

    _steps_required is the number of steps that are required to hatch the egg.
    _steps_remaining is the number of steps that are remaining to hatch the egg.
    _hatched is a boolean value which tells PartyManager whether or not to hatch the egg (turn it into a pokemon).

    CLASS VARIABLES:
    _MEMBER_TYPE: The type of party member. In this case, it is "Egg"

    _MIN_STEPS, _MAX_STEPS: Defines the range in which the _steps_required is generated between.

    """

    _steps = RandomStats.rand_steps()

    hatched = BooleanField(default=False)
    steps_required = IntegerField(column_name="steps_required", default=_steps)
    steps_remaining = IntegerField(column_name="steps_remaining", default=_steps)
    member_type = CharField(column_name='member_type', default='Egg')
    player = ForeignKeyField(PartyManager, backref='eggs')
    id = CharField(primary_key=True)

    def add_steps(self, steps: int) -> None:
        """ Decrements _steps_remaining by param steps. If _steps_remaining <= 0, _hatched property is set to True.

        :param int steps: Number of steps to decrement _steps_remaining by.
        :return: No return
        :rtype: None

        """
        if type(steps) != int:
            raise ValueError('Steps must be integer.')

        self.steps_remaining = self.steps_remaining - steps
        if self.steps_remaining <= 0 and not self.hatched:
            self._hatch()
        self.save()

    @property
    def description(self) -> str:
        """ Returns a description of the Egg """
        return f"Your {self.nickname} is {self.height}cm tall and {self.weight}kg. " \
               f"{ 'Currently in party.' if self.in_party else 'Not currently in party'}"

    def _hatch(self):
        if self.nickname == 'Egg':
            nickname = Pokedex[self.pokedex_num][0]
        else:
            nickname = self.nickname

        new_pokemon = Pokemon.create(id=self.player._ID_MANAGER.pokemon_id(), pokedex_num=self.pokedex_num, 
                        nickname=nickname, source=self.source,
                        date_acquired=self.date_acquired, item=self.item, player=self.player)
        new_pokemon.save()
        
        # self.player.release_pc_pokemon(self.id)
        # self.save()
        self.player.release_member(self.id)


    def to_dict(self) -> dict:
        """ Converts current instance attributes into dictionary format and returns it

        :return: Dictionary of all instance attributes
        :rtype: dict

        """
        dik = {
            "id": self.id,
            "player": self.player.player_name,
            "member_type": self.member_type,
            "pokedex_num": self.pokedex_num,
            "source": self.source,
            "nickname":  self.nickname,
            "item": self.item,

            "in_party": self.in_party,
            "weight": str(self.weight),
            "height": str(self.height),
            "date_acquired": str(self.date_acquired),

            "steps_required": self.steps_required,
            "steps_remaining": self.steps_remaining,
            "hatched": self.hatched
        }
        return dik
