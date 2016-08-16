from datetime import datetime

from peewee import *
from conf import settings


DB = SqliteDatabase(settings.DB)


class Task(Model):
    employee = CharField(max_length=50)
    project = CharField(max_length=100, default='')
    name = CharField(max_length=30)
    mins = IntegerField()
    notes = TextField(default='')
    date = DateField(default=datetime.today)

    class Meta:
        database = DB

    def save(self, *args, **kwargs):
        if self.project:
            self.project = '{}'.format(
                self.project.lower().replace(' ', '_'))
        super(Task, self).save(*args, **kwargs)

    @property
    def project_name(self):
        return '{}'.format(self.project).replace('_', ' ').title()
