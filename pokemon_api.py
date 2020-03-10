"""
Author: Tushya Iyer, Nolan Crooks
ACIT 2515
Date: 3/9/2020
"""
from flask import Flask, jsonify, request, make_response
from party_manager import PartyManager
from pokemon import Pokemon
from egg import Egg

app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)