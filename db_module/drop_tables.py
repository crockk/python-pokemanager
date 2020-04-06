from .db import db
from pokemodule.party_manager import PartyManager
from pokemodule.egg import Egg
from pokemodule.pokemon import Pokemon

db.drop_tables([PartyManager, Pokemon, Egg])