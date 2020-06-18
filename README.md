# Python PokéManager
> Pokémon themed minigame where you can build multiple player's battle parties, hatch eggs, 
>level up members, move them from PC Storage to party, and view stats, and more!
>
![Pokégui](https://i.imgur.com/xLJ5eN1.png "pokegui")


## Setup
> Clone this repository to your local machine using
```
git clone https://github.com/crockk/python-pokemanager.git
```
> After cloning the repository, navigate to the root directory of the project and run
```
pip install -r requirements.txt
```
> to install the necessary dependencies.


## Usage
- Follow these steps to get the application up and running:
> Run the file `pokemon_api.py` to start the API and initialize the database

> Run the file `pokegui.py` to launch the GUI

> Build your parties!

## Technical Mumbo Jumbo
- If you're reading this far, I'm not really sure why, but anyways, here's the Python class structure for
this program:

#### Abstract Class PartyMember:
> This class defines various base stats of the PartyMember that inherits it.

#### Subclass Pokemon:
> The Pokémon is a type of PartyMember, in other words, a subclass of PartyMember. It inherits all properties of a PartyMember,
>as well as adding many stats and attributes that are unique to Pokémon.

#### Subclass Egg:
> The Egg is the second type of PartyMember. It also inherits all properties
>of a PartyMember, but is relatively simple in that it only adds a few new properties (eg _steps_required).

#### PartyManager Class:
> This class manages one player's Pokemon Party and PC Storage (PC Storage is where Pokemon that are not in a party
are placed).

#### PokeStats Class:
> This is a simple class which provides statistics to display about the player and their Pokémon for the class
>PartyManager to display.


