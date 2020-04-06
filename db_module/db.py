from peewee import SqliteDatabase, Model
import os

db = SqliteDatabase(os.path.join("db_module", "pokemanager.db"))

db.connect()


class BaseModel(Model):
    class Meta:
        database = db