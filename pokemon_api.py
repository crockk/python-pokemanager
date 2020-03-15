"""
Author: Tushya Iyer, Nolan Crooks
ACIT 2515
Date: 3/9/2020
"""
from flask import Flask, jsonify, request, make_response
from party_manager import PartyManager
from pokemon import Pokemon
from egg import Egg
import os

app = Flask(__name__)

FILEPATH = os.path.join("data", "pokedata.json")
poke_inventory = PartyManager("Ashy Ketchup")


@app.route("/partymanager/member", methods=["POST"])
def add_pokemon_member():
    """ POST method for Party Member
    Creates a new Party Member with json data from the request

    :return: Response containing the http status code and either the ID of the new member or Error Message
    :rtype: Response Object
    
    """
    new_member = request.json
    try:
        new_id = poke_inventory.create_member(new_member["member_type"], new_member["pokedex_num"], new_member["source"], nickname=new_member["nickname"], item=new_member["item"], ability=new_member["ability"])
        return make_response(str(new_id), 200)
    except Exception as err:
        message = "missing attribute " + str(err)
        return make_response(message, 400)


@app.route("/partymanager/member/<int:member_id>", methods=["PUT"])
def update_member(member_id):
    """ PUT method for Party Member
    Updates an existing Party Member with json data from the request

    :return: Response containing the http status code and either nothing or Error Message
    :rtype: Response Object
    
    """
    data = request.json
    member = poke_inventory.get_member_by_id(member_id)
    if not member:
        return make_response("Party Member not found.", 400)

    if sorted(["nickname", "item"]) != sorted(data.keys()):
        return make_response("Invalid JSON", 400)

    try:
        if data["nickname"]:
            member.nickname = data["nickname"]
        if data["item"]:
            member.held_item = data["item"]
        return make_response("", 204)
    except Exception as err:
        return make_response(str(err), 400)


@app.route("/partymanager/member/<int:member_id>", methods=["DELETE"])
def remove_member(member_id):
    """ DELETE method for Party Member
    Deletes an existing Party Member

    :return: Response containing the http status code and either nothing or Error Message
    :rtype: Response Object
    
    """
    member = poke_inventory.get_member_by_id(member_id)
    if not member:
        return make_response("Party Member not found.", 400)

    if member.in_party:
        result = poke_inventory.release_party_member(member_id)
    else:
        result = poke_inventory.release_pc_pokemon(member_id)
    
    if result:
        return make_response("", 204)
    else:
        return make_response(f"Could not delete member with id: {member_id}")


@app.route("/partymanager/member/<int:member_id>", methods=["GET"])
def get_member(member_id):
    """ GET method for Party Member
    Returns a Party Member in json format 

    :return: Response containing the http status code and either the json representation of the member or Error Message
    :rtype: Response Object
    
    """
    member = poke_inventory.get_member_by_id(member_id)
    if not member:
        return make_response("Party Member not found.", 400)
    else:
        return jsonify(member.to_dict())


@app.route("/partymanager/member/all", methods=["GET"])
def all_members():
    """ GET method for Party Manager
    Returns the json representation of the Party

    :return: Response containing the http status code and either a list of all the party members or Error Message
    :rtype: Response Object
    
    """
    return jsonify([member.to_dict() for member in poke_inventory.get_all_members])


@app.route("/partymanager/member/all/<string:member_type>", methods=["GET"])
def all_members_by_type(member_type):
    """ POST method for Party Manager
    Returns a json representation of all the members of a specific sub-type. Either 'Pokemon' or 'Egg'

    :return: Response containing the http status code and a list of members of the specified type
    :rtype: Response Object
    
    """
    return jsonify([member.to_dict() for member in poke_inventory.get_member_by_type(member_type)])


@app.route("/partymanager/member/stats", methods=["GET"])
def manager_stats():
    """ POST method for Party Manager
    Returns a json representation of the stats for the Party Manager

    :return: Response containing the http status code and the stats of the Party Manager
    :rtype: Response Object
    
    """
    return jsonify(poke_inventory.get_stats().to_dict())

if __name__ == "__main__":
    app.run(debug=True)
