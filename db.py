from peewee import SqliteDatabase, Model

db = SqliteDatabase("pokemanager.db")

db.connect()


class BaseModel(Model):
    class Meta:
        database = db