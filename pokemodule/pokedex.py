from random import uniform, randint, sample

# Species Name, Types
Pokedex = {
    1: ["Bulbasaur", "Grass", 'img/1.png'],
    2: ["Charmander", "Fire", 'img/2.png'],
    3: ["Squirtle", "Water", 'img/3.png'],
    4: ["Pikachu", "Electric", 'img/4.png'],
    5: ["Turtwig", "Grass", 'img/5.png'],
    6: ["Chimchar", "Fire", 'img/6.png'],
    7: ["Piplup", "Water", 'img/7.png'],
    8: ["Kyogre", "Water", 'img/8.png'],
    9: ["Groudon", "Ground", 'img/9.png'],
    10: ["Rayquaza", "Flying/Dragon", 'img/10.png']
}

class IdManager():

    def __init__(self):
        self._e_id = 1
        self._p_id = 1

    def egg_id(self):
        id = f"e{str(self._e_id).zfill(4)}"
        self._e_id += 1
        return id

    def pokemon_id(self):
        id = f"p{str(self._p_id).zfill(4)}"
        self._p_id += 1
        return id

class RandomStats():

    _MIN_WEIGHT = 50  # KG
    _MAX_WEIGHT = 1000  # KG

    _MIN_HEIGHT = 80  # CM
    _MAX_HEIGHT = 1500  # CM

    _MIN_BASE_XP = 80
    _MAX_BASE_XP = 120

    _MIN_LEVEL_UP_XP_MULT = 1.0
    _MAX_LEVEL_UP_XP_MULT = 1.5

    _STARTING_LEVEL = 5

    _MIN_BATTLE_STAT = 3
    _MAX_BATTLE_STAT = 18

    _MIN_BASE_HP = 15
    _MAX_BASE_HP = 35

    _MOVE_SET_LENGTH = 4

    _MIN_STEPS = 1000  # steps
    _MAX_STEPS = 5000  # steps
    
    # Move Name, Damage
    MOVES = {
        1: ('Tail Whip', 0),
        2: ('Growl', 0),
        3: ('Splash', 0),
        4: ('Leer', 0)
    }
    @classmethod
    def rand_weight(cls) -> float:
        """ Classmethod that calculates a random weight

        :return: Returns random weight
        :rtype: Float

        """
        return round(uniform(cls._MIN_WEIGHT, cls._MAX_WEIGHT), 2)

    @classmethod
    def rand_height(cls) -> float:
        """ Classmethod that calculates a random height

        :return: Returns random height
        :rtype: Float

        """
        return round(uniform(cls._MIN_HEIGHT, cls._MAX_HEIGHT), 2)

    @classmethod
    def rand_base_xp(cls) -> int:
        """ Generates random base xp based on class variables

        :return: Base xp level
        :rtype: Integer

        """
        return randint(cls._MIN_BASE_XP, cls._MAX_BASE_XP)

    @classmethod
    def rand_xp_level_up_multiplier(cls) -> float:
        """ Generates xp level up multiplier based on class variables

        :return: Xp level up multiplier
        :rtype: Float

        """
        return round(uniform(cls._MIN_LEVEL_UP_XP_MULT, cls._MAX_LEVEL_UP_XP_MULT), 2)

    @classmethod
    def rand_battle_stat(cls) -> int:
        """ Generates random base battle stat based on class variables

        :return: Base stat
        :rtype: Integer

        """
        return randint(cls._MIN_BATTLE_STAT, cls._MAX_BATTLE_STAT)

    @classmethod
    def rand_base_hp(cls) -> int:
        """ Generates random base HP based on class variables

        :return: Base HP
        :rtype: Integer

        """
        return randint(cls._MIN_BASE_HP, cls._MAX_BASE_HP)

    @classmethod
    def rand_move_set(cls) -> list:
        """ Randomly selects _MOVE_SET_LENGTH number of moves from the Moves stored in pokedex module

        :return: Move list from Moves
        :rtype: list

        """
        move_indices = sample(list(cls.MOVES), cls._MOVE_SET_LENGTH)

        return [cls.MOVES[move_index] for move_index in move_indices]

    @classmethod
    def rand_steps(cls) -> int:
        """ Class method which calculates a random integer between class variables _MIN_STEPS and _MAX_STEPS """
        return randint(cls._MIN_STEPS, cls._MAX_STEPS)