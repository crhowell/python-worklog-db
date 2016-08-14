from datetime import datetime

from conf import settings
from logs.models.task import Task


class Log:

    def update_task(self, data={}):
        if data:
            q = Task.update(**data['edits']).where(Task.id == data['id'])
            q.execute()
            return True
        return False

    def delete_task(self, task_id=None):
        if task_id is not None:
            task = self.find_task('id', task_id)
            task.delete_instance()
            return True
        else:
            return False

    def find_task(self, by=None, search=''):
        result = []
        if by is not None:
            if by == 'employee':
                return self.task.select(Task).where(
                    Task.employee.contains(search))
            elif by == 'rdate':
                return self.task.select().where(
                    self.task.date.between(search[0], search[1]))
            elif by == 'rtime':
                return self.task.select(Task).where(
                    Task.mins >= search[0], Task.mins <= search[1])
            elif by == 'date':
                return self.task.select(Task).where(Task.date == search)
            elif by == 'term':
                return self.task.select(Task).where(Task.name == search)
            elif by == 'id':
                return self.task.get(Task.id == search)
            # elif by == 'project':
            #     return self.task.select(Task).where(Task.project == search)
        else:
            return False

        return result

    def all_tasks(self):
        tasks = self.task.select().order_by(Task.date.desc())
        return tasks

    def add_task(self, task={}):
        if task:
            for k, v in task.items():
                if v is None:
                    return False
            new_task = self.task.create(**task)
            return True if isinstance(new_task, Task) else False
        else:
            return False

    def connect(self):
        self.db.connect()
        self.db.create_tables([Task], safe=True)

    @staticmethod
    def valid_date(date):
        """Returns True if date is actually a date,
        based-on a pre-defined date format.
        """
        try:
            datetime.strptime(date, '%m/%d/%Y')
        except ValueError:
            return False
        return True

    @staticmethod
    def valid_num(num):
        """Returns True if the input was in-fact an integer."""
        try:
            val = int(num)
        except ValueError:
            return False
        return True

    @staticmethod
    def valid_name(name=''):
        """Returns True if non-empty string was given."""
        return True if name else False

    @staticmethod
    def convert_date(date, fmt='%m/%d/%Y'):
        try:
            date = datetime.strptime(date, fmt)
            return date
        except ValueError:
            return False


    def __init__(self):
        self.db = settings.DB
        self.connect()
        self.task = Task
