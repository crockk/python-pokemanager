from db.db import db
from pokemodule.party_manager import PartyManager
from pokemodule.egg import Egg
from pokemodule.pokemon import Pokemon


def create_tables():
    db.create_tables([PartyManager, Pokemon, Egg])