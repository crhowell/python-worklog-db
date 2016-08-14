from datetime import datetime

from peewee import *

from conf import settings


class Task(Model):
    employee = CharField(max_length=50)
    name = CharField(max_length=30)
    mins = IntegerField()
    notes = TextField(default='')
    date = DateField(default=datetime.now)

    class Meta:
        database = settings.DB
