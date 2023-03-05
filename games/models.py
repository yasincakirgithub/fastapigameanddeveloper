import peewee

from database import db
from developers.models import Developer

class Game(peewee.Model):
    name = peewee.CharField(index=True)
    description = peewee.CharField(index=True)
    publication_date = peewee.DateField(index=True)
    developer = peewee.ForeignKeyField(Developer, backref="items")
    status = peewee.BooleanField(default=False)

    class Meta:
        database = db