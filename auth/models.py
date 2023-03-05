import peewee

from database import db


class User(peewee.Model):
    id = peewee.AutoField()
    username = peewee.CharField(unique=True, index=True)
    first_name = peewee.CharField(index=True)
    last_name = peewee.CharField(index=True)
    password = peewee.CharField(index=True)

    class Meta:
        database = db