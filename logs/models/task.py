from datetime import datetime

from peewee import *
from conf import settings


db = SqliteDatabase(settings.DB)


class Task(Model):
    employee = CharField(max_length=50)
    project = CharField(max_length=100, default='')
    name = CharField(max_length=30)
    mins = IntegerField()
    notes = TextField(default='')
    date = DateField(default=datetime.now)

    class Meta:
        database = db

    def save(self, *args, **kwargs):
        if self.project:
            self.project = '{}'.format(
                self.project.lower().replace(' ', '_'))
        super(Task, self).save(*args, **kwargs)

    @property
    def project_name(self):
        return '{}'.format(self.project).replace('_', ' ').title()
