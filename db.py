from peewee import SqliteDatabase

db = SqliteDatabase("pokemanager.db")

db.connect()