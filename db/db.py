from peewee import SqliteDatabase, Model
import os

db = SqliteDatabase("../pokemanager.db")

db.connect()


class BaseModel(Model):
    class Meta:
        database = db