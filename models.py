import peewee

from database import db


class Developer(peewee.Model):
    username = peewee.CharField(unique=True, index=True)
    full_name = peewee.BooleanField(default=True)
    age = peewee.IntegerField()

    class Meta:
        database = db


class Game(peewee.Model):
    name = peewee.CharField(index=True)
    description = peewee.CharField(index=True)
    publication_date = peewee.DateField(index=True)
    developer = peewee.ForeignKeyField(Developer, backref="items")
    status = peewee.BooleanField(default=False)

    class Meta:
        database = db