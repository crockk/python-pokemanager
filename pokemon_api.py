"""
Author: Tushya Iyer, Nolan Crooks
ACIT 2515
Date: 3/9/2020
"""
from flask import Flask, jsonify, request, make_response
from pokemodule.party_manager import PartyManager
from pokemodule.pokemon import Pokemon
from pokemodule.egg import Egg
from pokemodule.pokedex import Pokedex
from create_tables import create_tables
from drop_tables import drop_tables

app = Flask(__name__)
drop_tables()
create_tables()


def initialize_default_managers():
    poke_inventory = PartyManager(player_name="Dash Ketchup")
    poke_inventory.save()
    pika = Pokemon.create(pokedex_num=10, nickname=Pokedex[10][0], player=poke_inventory, id=poke_inventory._ID_MANAGER.pokemon_id(), source='Vancouver', item='White Claw')
    pika.save()
    poke1 = Pokemon.create(pokedex_num=6, nickname=Pokedex[6][0], player=poke_inventory, id=poke_inventory._ID_MANAGER.pokemon_id(), source='Coquitlam', item='Water Whip')
    poke1.save()
    poke2 = Pokemon.create(pokedex_num=5, nickname=Pokedex[5][0], player=poke_inventory, id=poke_inventory._ID_MANAGER.pokemon_id(), source='Port Moody', item='Shiny Stone')
    poke2.save()
    poke3 = Pokemon.create(pokedex_num=7, nickname=Pokedex[7][0], player=poke_inventory, id=poke_inventory._ID_MANAGER.pokemon_id(), source='Tokyo', item='Sakura Petal')
    poke3.save()
    poke4 = Pokemon.create(pokedex_num=2, nickname=Pokedex[2][0], player=poke_inventory, id=poke_inventory._ID_MANAGER.pokemon_id())
    poke4.save()
    poke5 = Pokemon.create(pokedex_num=1, nickname=Pokedex[1][0], player=poke_inventory, id=poke_inventory._ID_MANAGER.pokemon_id())
    poke5.save()
    poke6 = Pokemon.create(pokedex_num=9, nickname=Pokedex[9][0], player=poke_inventory, id=poke_inventory._ID_MANAGER.pokemon_id())
    poke6.save()
    egg1 = Egg.create(pokedex_num=2, nickname='Egg', player=poke_inventory, id=poke_inventory._ID_MANAGER.egg_id(), source='Route 78')
    egg1.save()

    poke_inventory = PartyManager(player_name="Trainer Nolan")
    poke_inventory.save()
    pika = Pokemon.create(pokedex_num=8, nickname=Pokedex[8][0], player=poke_inventory, id=poke_inventory._ID_MANAGER.pokemon_id(), source='White Horse', item='Hoof')
    pika.save()
    poke1 = Pokemon.create(pokedex_num=5, nickname=Pokedex[5][0], player=poke_inventory, id=poke_inventory._ID_MANAGER.pokemon_id(), source='Calgary', item='Water Whip')
    poke1.save()
    poke2 = Pokemon.create(pokedex_num=3, nickname=Pokedex[3][0], player=poke_inventory, id=poke_inventory._ID_MANAGER.pokemon_id(), source='Port Moody', item='Shiny Stone')
    poke2.save()
    poke3 = Pokemon.create(pokedex_num=9, nickname=Pokedex[9][0], player=poke_inventory, id=poke_inventory._ID_MANAGER.pokemon_id(), source='Tokyo', item='Sakura Petal')
    poke3.save()
    poke4 = Pokemon.create(pokedex_num=2, nickname=Pokedex[2][0], player=poke_inventory, id=poke_inventory._ID_MANAGER.pokemon_id())
    poke4.save()
    poke6 = Pokemon.create(pokedex_num=10, nickname=Pokedex[1][0], player=poke_inventory, id=poke_inventory._ID_MANAGER.pokemon_id())
    poke6.save()
    egg1 = Egg.create(pokedex_num=2, nickname='Egg', player=poke_inventory, id=poke_inventory._ID_MANAGER.egg_id(), source='Route 78')
    egg1.save()
    egg2 = Egg.create(pokedex_num=10, nickname='Egg', player=poke_inventory, id=poke_inventory._ID_MANAGER.egg_id(), source='Victory Road')
    egg2.save()

    poke_inventory = PartyManager(player_name="Rival Tushya")
    poke_inventory.save()
    pika = Pokemon.create(pokedex_num=8, nickname=Pokedex[8][0], player=poke_inventory, id=poke_inventory._ID_MANAGER.pokemon_id(), source='White Horse', item='Hoof')
    pika.save()
    poke1 = Pokemon.create(pokedex_num=5, nickname=Pokedex[5][0], player=poke_inventory, id=poke_inventory._ID_MANAGER.pokemon_id(), source='Calgary', item='Water Whip')
    poke1.save()
    poke2 = Pokemon.create(pokedex_num=3, nickname=Pokedex[3][0], player=poke_inventory, id=poke_inventory._ID_MANAGER.pokemon_id(), source='Port Moody', item='Shiny Stone')
    poke2.save()
    poke3 = Pokemon.create(pokedex_num=9, nickname=Pokedex[9][0], player=poke_inventory, id=poke_inventory._ID_MANAGER.pokemon_id(), source='Tokyo', item='Sakura Petal')
    poke3.save()
    poke4 = Pokemon.create(pokedex_num=3, nickname=Pokedex[2][0], player=poke_inventory, id=poke_inventory._ID_MANAGER.pokemon_id())
    poke4.save()
    poke6 = Pokemon.create(pokedex_num=10, nickname=Pokedex[1][0], player=poke_inventory, id=poke_inventory._ID_MANAGER.pokemon_id())
    poke6.save()
    egg1 = Egg.create(pokedex_num=2, nickname='Egg', player=poke_inventory, id=poke_inventory._ID_MANAGER.egg_id(), source='Route 78')
    egg1.save()
    egg2 = Egg.create(pokedex_num=10, nickname='Egg', player=poke_inventory, id=poke_inventory._ID_MANAGER.egg_id(), source='Victory Road')
    egg2.save()


@app.route('/create_manager', methods=["POST"])
def add_manager():
    """ POST method for Manager
    Creates a new Manager with json data from the request

    :return: Response containing the http status code and either the ID of the new pokemon or Error Message
    :rtype: Response Object

    """
    data = request.json
    if data['player_name'] == '':
        return make_response('no name', 401)
    try:
        new_player = PartyManager.create(player_name=data['player_name'])
        new_player.save()
        return make_response(str(new_player), 200)
    except Exception as err:
        message = "missing attribute " + str(err)
        return make_response(message, 400)

@app.route("/<int:manager_id>/pokemon", methods=["POST"])
def add_pokemon(manager_id):
    """ POST method for Pokemon
    Creates a new Pokemon with json data from the request

    :return: Response containing the http status code and either the ID of the new pokemon or Error Message
    :rtype: Response Object
    
    """
    player = PartyManager.get_by_id(manager_id)
    new_member = request.json
    if new_member['nickname'] == '':
        new_member['nickname'] = Pokedex[int(new_member['pokedex_num'])][0]
    if new_member['source'] == '':
        new_member['source'] = 'Pallet Town'
    try:
        new_id = Pokemon.create(pokedex_num=new_member["pokedex_num"],
                                 nickname=new_member["nickname"],
                                 player=player,
                                 id=player._ID_MANAGER.pokemon_id(),
                                 source=new_member["source"],
                                 item=new_member["item"],
                                 ability=new_member["ability"])
        new_id.save()
        return make_response(str(new_id), 200)
    except Exception as err:
        message = "missing attribute " + str(err)
        return make_response(message, 400)


@app.route("/<int:manager_id>/egg", methods=["POST"])
def add_egg(manager_id):
    """ POST method for Egg
    Creates a new Egg with json data from the request

    :return: Response containing the http status code and either the ID of the new egg or Error Message
    :rtype: Response Object

    """
    player = PartyManager.get_by_id(manager_id)
    new_member = request.json
    if new_member['nickname'] == '':
        new_member['nickname'] = 'Egg'
    if new_member['source'] == '':
        new_member['source'] = 'Pallet Town'
    try:
        new_id = Egg.create(pokedex_num=new_member["pokedex_num"],
                             nickname=new_member["nickname"],
                             player=player,
                             id=player._ID_MANAGER.egg_id(),
                             source=new_member["source"])
        new_id.save()
        return make_response(str(new_id), 200)
    except Exception as err:
        message = "missing attribute " + str(err)
        return make_response(message, 400)


@app.route("/<int:manager_id>/member/<member_id>", methods=["PUT"])
def update_member(manager_id, member_id):
    """ PUT method for Party Member
    Updates an existing Party Member with json data from the request

    :return: Response containing the http status code and either nothing or Error Message
    :rtype: Response Object
    
    """
    data = request.json
    player = PartyManager.get_by_id(manager_id)
    member = player.get_member_by_id(member_id)
    if not member:
        return make_response("Party Member not found.", 400)

    if sorted(["nickname", "item"]) != sorted(data.keys()):
        return make_response("Invalid JSON", 400)

    try:
        if data["nickname"]:
            member.nickname = data["nickname"]
            member.save()
        if data["item"]:
            member.item = data["item"]
            member.save()
        return make_response("", 204)
    except Exception as err:
        return make_response(str(err), 400)


@app.route("/<int:manager_id>/member/<member_id>/add_xp", methods=["PUT"])
def add_xp(manager_id, member_id):
    """ PUT method for Party Member
    Adds a set amount of XP to the party member

    :return: Response containing the http status code and either nothing or Error Message
    :rtype: Response Object

    """
    player = PartyManager.get_by_id(manager_id)
    member = player.get_member_by_id(member_id)
    if not member:
        return make_response("Party Member not found.", 400)
    member.add_xp(100)
    return make_response("", 204)


@app.route("/<int:manager_id>/member/<member_id>/damage", methods=["PUT"])
def damage(manager_id, member_id):
    """ PUT method for Party Member
    Damages a party member by a set amount

    :return: Response containing the http status code and either nothing or Error Message
    :rtype: Response Object

    """
    player = PartyManager.get_by_id(manager_id)
    member = player.get_member_by_id(member_id)
    if not member:
        return make_response("Party Member not found.", 400)
    member.damage(10)
    return make_response("", 204)


@app.route("/<int:manager_id>/member/<member_id>/heal", methods=["PUT"])
def heal(manager_id, member_id):
    """ PUT method for Party Member
    Heal a party member by a set amount

    :return: Response containing the http status code and either nothing or Error Message
    :rtype: Response Object

    """
    player = PartyManager.get_by_id(manager_id)
    member = player.get_member_by_id(member_id)
    if not member:
        return make_response("Party Member not found.", 400)
    member.heal(10)
    return make_response("", 204)


@app.route("/<"
           "int:manager_id>/member/<member_id>", methods=["DELETE"])
def remove_member(manager_id, member_id):
    """ DELETE method for Party Member
    Deletes an existing Party Member

    :return: Response containing the http status code and either nothing or Error Message
    :rtype: Response Object
    
    """
    player = PartyManager.get_by_id(manager_id)
    if not player:
        return make_response(f"Party Manager with id '{manager_id}' not found.", 400)
    member = player.get_member_by_id(member_id)
    if not member:
        return make_response(f"Party Member with id '{member_id}' not found.", 400)

    result = player.release_member(member_id)
    
    if result:
        return make_response("", 204)
    else:
        return make_response(f"Could not delete member with id '{member_id}'", 401)


@app.route("/<int:manager_id>/member/<member_id>", methods=["GET"])
def get_member(manager_id, member_id):
    """ GET method for Party Member
    Returns a Party Member in json format 

    :return: Response containing the http status code and either the json representation of the member or Error Message
    :rtype: Response Object
    
    """
    player = PartyManager.get_by_id(manager_id)
    if not player:
        return make_response(f"Party Manager with id '{manager_id}' not found.", 400)
    member = player.get_member_by_id(member_id)
    if not member:
        return make_response(f"Party Member with id '{member_id}' not found.", 400)
    else:
        return jsonify(member.to_dict())


@app.route("/<int:manager_id>/member/all", methods=["GET"])
def all_members(manager_id):
    """ GET method for Party Manager
    Returns the json representation of the Party

    :return: Response containing the http status code and either a list of all the party members or Error Message
    :rtype: Response Object
    
    """
    player = PartyManager.get_by_id(manager_id)
    if not player:
        return make_response(f"Party Manager with id '{manager_id}' not found.", 400)
    
    members = player.all_members
    # if not members:
    #     return make_response(f"No Members found.", 400)
    
    return jsonify([member.to_dict() for member in members])


@app.route("/<int:manager_id>/member/all/<string:member_type>", methods=["GET"])
def all_members_by_type(manager_id, member_type):
    """ POST method for Party Manager
    Returns a json representation of all the members of a specific sub-type. Either 'Pokemon' or 'Egg'

    :return: Response containing the http status code and a list of members of the specified type
    :rtype: Response Object
    
    """
    player = PartyManager.get_by_id(manager_id)
    if not player:
        return make_response(f"Party Manager with id '{manager_id}' not found.", 400)
    
    members = player.get_member_by_type(member_type)
    if not members:
        return make_response(f"No Members found for with type '{member_type}'.", 400)

    return jsonify([member.to_dict() for member in members])


@app.route("/<int:manager_id>/member/stats", methods=["GET"])
def manager_stats(manager_id):
    """ POST method for Party Manager
    Returns a json representation of the stats for the Party Manager

    :return: Response containing the http status code and the stats of the Party Manager
    :rtype: Response Object
    
    """
    player = PartyManager.get_by_id(manager_id)
    if player:
        return jsonify(player.get_stats().to_dict())
    else:
        return make_response(f"Party Manager with id '{manager_id}' not found.", 400)


@app.route('/managers', methods=["GET"])
def all_managers():
    """ GET method for Party Manager
    Returns a json of all the managers in the DB

    """
    return jsonify([manager.to_dict() for manager in PartyManager.select()])


@app.route('/managers/<int:manager_id>', methods=["GET"])
def get_manager(manager_id):
    """ GET method for Party Manager
    Returns a json of all the managers in the DB

    """
    return jsonify((PartyManager.select().where(PartyManager.id == manager_id))[0].to_dict())


@app.route('/<int:manager_id>/<member_id>/move', methods=["PUT"])
def move_member(manager_id, member_id):
    """ PUT method for moving a member to the manager's party, or removing from the party, depending on it's status """
    player = PartyManager.get_by_id(manager_id)
    member = player.get_member_by_id(member_id)
    if not member:
        return make_response("Party Member not found.", 400)

    try:
        if member.in_party:
            member.in_party = False
            member.save()
            return make_response("Member moved to party", 204)
        else:
            if len(player.party_members) == 6:
                return make_response('Your party is full', 401)
            member.in_party = True
            member.save()
            return make_response("Member moved to party", 204)
    except Exception as err:
        return make_response(str(err), 400)


if __name__ == "__main__":
    initialize_default_managers()
    app.run(debug=True)
