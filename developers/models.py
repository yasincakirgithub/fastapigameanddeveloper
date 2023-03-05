import peewee

from database import db


class Developer(peewee.Model):
    username = peewee.CharField(unique=True, index=True)
    full_name = peewee.BooleanField(default=True)
    age = peewee.IntegerField()

    class Meta:
        database = db