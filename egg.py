"""
Author: Tushya Iyer, Nolan Crocks
ACIT 2515
Date: 2/17/2020
"""

from party_member import PartyMember
from typing import List


class Egg(PartyMember):
    def __init__(self, id: int, species_id: int, source: str, nickname: str = None, item: str = None) -> None:
        pass

    # Hatch needs to create a new pokemon and add it to the party manager. Wrong place for this funcion?
    # Add bool to declare this as hatched and add a function in manager to periodically check?
    def _hatch(self) -> None:
        pass

    @property
    def steps_required(self) -> int:
        pass

    @property
    def steps_remaining(self) -> int:
        pass

    def walk(self, steps: int) -> None:
        pass
