"""
Author: Tushya Iyer, Nolan Crooks
ACIT 2515
Date: 2/17/2020
"""


class PokeStats:
    """ Defines the PokeStats class for use in PartyManager """

    def __init__(self, total_by_type: dict, total_eggs: int, total_KO: int, total_steps: int, player_name: str) -> None:
        """ Initalizes instance properties

        :return: No return
        :rtype: None

        """

        self._total_by_type = total_by_type

        self._total_eggs = total_eggs

        self._total_KO = total_KO

        self._total_steps = total_steps

        self._player_name = player_name

    def to_dict(self) -> dict:
        """ Converts instance attributes to dictionary format and returns it

        :return: Dictionary of instance attributes
        :rtype: dict
        """
        return {
            "player_name": self._player_name,
            "total_by_type": self._total_by_type,
            "total_eggs": self._total_eggs,
            "total_KO": self._total_KO,
            "total_steps": self._total_steps
        }

    def get_total_by_type(self) -> dict:
        """ Gets and returns total pokemon by type

        :return: Total by type
        :rtype: Dictionary

        """
        return self._total_by_type

    def get_total_eggs(self) -> int:
        """ Gets and returns total eggs

        :return: Total eggs
        :rtype: Integer

        """
        return self._total_eggs

    def get_total_KO(self) -> int:
        """ Gets and returns total pokemon KO'd

        :return: Total KO'd
        :rtype: Integer

        """
        return self._total_KO

    def get_total_steps(self) -> int:
        """ Gets and returns total steps the player has taken

        :return: Total steps
        :rtype: Integer

        """
        return self._total_steps
