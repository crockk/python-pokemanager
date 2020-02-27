"""
Author: Tushya Iyer, Nolan Crooks
ACIT 2515
Date: 2/13/2020
"""
from abc import abstractmethod, ABC
from datetime import date, datetime
from random import uniform


class PartyMember(ABC):
    """ Defines the abstract class PartyMember

    This class defines various base stats of the PartyMember that inherits it.

    CLASS VARIABLES
    _MIN_WEIGHT and _MAX_WEIGHT: Range defining the weight of the party member

    _MIN_HEIGHT and _MAX_HEIGHT: Range defining the height of the party member

    """
    _MIN_WEIGHT = 50  # KG
    _MAX_WEIGHT = 1000  # KG

    _MIN_HEIGHT = 80  # CM
    _MAX_HEIGHT = 1500  # CM

    def __init__(self, id: int, pokedex_num: int, source: str, nickname: str, item: str = None, in_party: bool = None, weight: float = None, height: float = None, date_acquired: date = None) -> None:
        """ Initalizes instance properties

        :param int id: Unique identifier for pokemon
        :param int pokedex_num: Number corresponding with the pokedex entry of that member
        :param str source: The location that the member was acquired
        :param str nickname: A given nickname
        :param str item: The item that the member is holding
        :return: No return
        :rtype: None

        """
        self._validate_int(id, 1, "ID must be an Integer greater than or equal to 1")

        self._validate_int(pokedex_num, 1, "Pokedex Number must be greater than or equal to 1")

        self._validate_string(source, "Source must be a none-blank String")

        self._validate_string(nickname, "Nickname must be a none-blank String")

        if item is not None:
            self._validate_string(item, "Item must be a none-blank String")

        if in_party is not None:
            self._validate_bool(in_party, "In Party must be a valid Boolean")
            self._in_party = in_party
        else:
            self._in_party = False
        
        if weight is not None:
            self._validate_float(weight, self._MIN_WEIGHT, f"Weight must be a Float between {self._MIN_WEIGHT} and {self._MAX_WEIGHT}")
            self._weight = weight
        else:
            self._weight = self._rand_weight()

        if height is not None:
            self._validate_float(height, self._MIN_HEIGHT, f"Height must be a Float between {self._MIN_HEIGHT} and {self._MAX_HEIGHT}")
            self._height = height
        else:
            self._height = self._rand_height()

        if date_acquired is not None:
            self._validate_date(date_acquired, "Date Acquired must be a valid Date")
            self._date_acquired = date_acquired
        else:
            self._date_acquired = datetime.now().date()
        

        self._id = id
        self._pokedex_num = pokedex_num
        self._source = source
        self._nickname = nickname
        self._item = item

    @property
    def id(self) -> int:
        """ Gets and returns ID

        :return: ID
        :rtype: Integer

        """
        return self._id

    @property
    def pokedex_num(self) -> int:
        """ Gets and returns the pokedex number

        :return: Pokedex number
        :rtype: Integer

        """
        return self._pokedex_num

    @property
    def nickname(self) -> str:
        """ Gets and returns

        :return: Nickname
        :rtype: String

        """
        return self._nickname

    @nickname.setter
    def nickname(self, new_nickname: str) -> None:
        """ Sets a new nickname

        :param str new_nickname: New nickname for member
        :return: No return
        :rtype: None

        """
        self._validate_string(new_nickname, "Nickname must be a none-blank String")

        self._nickname = new_nickname

    @property
    def in_party(self) -> bool:
        """ Gets and returns the in_party property

        :return: in_party property
        :rtype: Boolean

        """
        return self._in_party

    @property
    def weight(self) -> float:
        """ Gets and returns weight property

        :return: Weight property
        :rtype: Float

        """
        return self._weight

    @property
    def height(self) -> float:
        """ Gets and returns height property

        :return: Height property
        :rtype: Float

        """
        return self._height

    @abstractmethod
    def description(self) -> str:
        """ Abstract method description implemented by child classes

        :raise: NotImplementedError
        :return: None
        :rtype: None
        """
        raise NotImplementedError

    @property
    def source(self) -> str:
        """ Gets and returns source property

        :return: Source property
        :rtype: String

        """
        return self._source

    @property
    def date_acquired(self) -> date:
        """ Gets and returns date_acquired

        :return: Returns the date acquired
        :rtype: Date

        """
        return self._date_acquired

    @property
    def held_item(self) -> str:
        """ Gets and returns held_item

        :return: The member's held item
        :rtype: String

        """
        if self._item:
            return self._item
        else:
            return "None"

    @held_item.setter
    def held_item(self, item: str) -> None:
        """ Set held_item property for the member

        :param str item: The new held item
        :return: No return
        :rtype: None

        """
        self._validate_string(item, "Item must be a none-blank String")

        self._item = item

    @classmethod
    def _rand_weight(cls) -> float:
        """ Classmethod that calculates a random weight

        :return: Returns random weight
        :rtype: Float

        """
        return round(uniform(cls._MIN_WEIGHT, cls._MAX_WEIGHT), 2)

    @classmethod
    def _rand_height(cls) -> float:
        """ Classmethod that calculates a random height

        :return: Returns random height
        :rtype: Float

        """
        return round(uniform(cls._MIN_HEIGHT, cls._MAX_HEIGHT), 2)

    @staticmethod
    def _validate_int(num: int, min_val: int, error_msg: str, max_val: int = None) -> None:
        """ Private method used to validate integers according to a minimum value and type

        :param int num: The number to be validated
        :param int min_val: The minimum value to be evaluated to
        :param str error_msg: Error message to be returned if exception raised
        :raises: TypeError, ValueError
        :return: No return
        :rtype: None

        """
        if type(num) is not int:
            raise TypeError(error_msg + f"\nNot type {type(num)}")
        if num < min_val:
            raise ValueError(error_msg)
        if max_val is not None:
            if num > max_val:
                raise ValueError(error_msg)

    @staticmethod
    def _validate_float(num: float, min_val: float, error_msg: str, max_val: float = None) -> None:
        """ Private method used to validate floats according to a minimum value and type

        :param float num: The number to be validated
        :param float min_val: The minimum value to be evaluated to
        :param str error_msg: Error message to be returned if exception raised
        :raises: TypeError, ValueError
        :return: No return
        :rtype: None

        """
        if type(num) is not float:
            raise TypeError(error_msg + f"\nNot type {type(num)}")
        if num < min_val:
            raise ValueError(error_msg)
        if max_val is not None:
            if num > max_val:
                raise ValueError(error_msg)
    
    @staticmethod
    def _validate_date(dt: date, error_msg: str) -> None:
        """ Private method used to validate dates

        :param date dt: The number to be validated
        :param str error_msg: Error message to be returned if exception raised
        :raises: TypeError, ValueError
        :return: No return
        :rtype: None

        """
        if type(dt) is not date:
            raise TypeError(error_msg + f"\nNot type {type(dt)}")
        
    @staticmethod
    def _validate_string(string: str, error_msg: str) -> None:
        """ Private method used to validate strings according to type

        :param str string: String to be validated
        :param str error_msg: Error message to be returned if exception raised
        :raises: TypeError, ValueError
        :return: No return
        :rtype: None
        """
        if type(string) is not str:
            raise TypeError(error_msg + f"\nNot type {type(string)}")
        if not string:
            raise ValueError(error_msg)
    
    @staticmethod
    def _validate_bool(val: bool, error_msg: str) -> None:
        """ Private method used to validate strings according to type

        :param str val: Boolean to be validated
        :param str error_msg: Error message to be returned if exception raised
        :raises: TypeError
        :return: No return
        :rtype: None
        """
        if type(val) is not bool:
            raise TypeError(error_msg + f"\nNot type {type(val)}")

    @abstractmethod
    def member_type(self):
        """ Abstract method member_type implemented in child classes

        :raise: NotImplementedError
        :return: None
        :rtype: None
        """
        raise NotImplementedError

    @abstractmethod
    def to_dict(self):
        """ Abstract method to_dict implemented in child classes

        :raise: NotImplementedError
        :return: None
        :rtype: None
        """
        raise NotImplementedError
