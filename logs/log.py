from datetime import datetime

from logs.models.task import Task, DB
from peewee import *


class Log:
    """Log acts as a layer between WorkLog and Task.

    Log contains validation for a Task and calls the
    Task model methods to perform CRUD operations.
    """

    def update_task(self, task_id=None, edits={}):
        """Updates a Task by ID and given 'edits' values.

        Keyword arguments:
        task_id -- Model ID of the Task
        edits -- Dict of Task values
        """
        if task_id is not None and edits:
            q = Task.update(**edits).where(Task.id == task_id)
            q.execute()
            return True
        return False

    def delete_task(self, task_id=None):
        """Deletes a Task instance by ID.

        Keyword arguments:
        task_id -- Model ID of the Task
        """
        if task_id is not None:
            try:
                task = self.find_task('id', task_id)
                task.delete_instance()
                return True
            except DoesNotExist:
                return False
        else:
            return False

    def find_task(self, by=None, search=''):
        """Find a Task in Database by method and search term.

        Keyword arguments:
        by -- method of field in which to search.
        search -- search term in which to look for.
        """

        if by is not None:
            if by == 'employee':
                return self.task.select().where(
                    Task.employee.contains(search))
            elif by == 'rdate':
                return self.task.select().where(
                    self.task.date.between(search[0], search[1]))
            elif by == 'rtime':
                return self.task.select().where(
                    Task.mins >= search[0], Task.mins <= search[1])
            elif by == 'date':
                return self.task.select().where(Task.date == search)
            elif by == 'term':
                return self.task.select().where(
                    (Task.name.contains(search)) |
                    (Task.notes.contains(search))
                )
            elif by == 'id':
                return self.task.get(Task.id == search)
            elif by == 'project':
                return self.task.select().where(
                    Task.project.contains(search))
            else:
                return False
        else:
            return False

    def all_tasks(self):
        """Retrieves all Tasks from database"""
        tasks = self.task.select().order_by(Task.date.desc())
        return tasks

    def add_task(self, task):
        """Given a Dict of Task values,
        creates a new Task and saves to database.

        Keyword arguments:
        task -- Dict of Task values.
        """

        if task:
            for k, v in task.items():
                if v is None:
                    return False

            new_task = self.task.create(**task)
            return new_task
        else:
            return False

    @staticmethod
    def parse_project_name(name=None):
        """Converts a project name into a consistent format,
        'Project Name' becomes 'project_name'.

        Keyword arguments:
        name -- User input project name
        """

        if name is not None:
            return name.lower().replace(' ', '_')
        else:
            return ''

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
        """Returns a Date obj, given a string date and format.

        Keyword arguments:
        date -- a string date
        fmt -- format of the passed in date
        """

        try:
            date = datetime.strptime(date, fmt)
            return date
        except ValueError:
            return False

    def initialize(self):
        """Creates or connects to database,
        defined in conf/settings.py.
        """
        db = DB
        db.connect()
        db.create_tables([Task], safe=True)

    def __init__(self):
        self.initialize()
        self.task = Task
