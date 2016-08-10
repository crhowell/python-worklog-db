from models.task import Task
import settings


class Log:

    def add_task(self):
        emp_name = input(' Employee Name: ')
        t_name = input(' Task Name: ')
        t_time = input(' Time Spent (in minutes): ')
        date = input(' Task Date: ')
        notes = input(' Notes: ')
        task = Task.create(employee=emp_name,
                           name=t_name,
                           mins=t_time,
                           date=date,
                           notes=notes)

    def connect(self):
        self.db.connect()
        self.db.create_tables([Task], safe=True)

    def __init__(self):
        self.db = settings.DB
        self.connect()
