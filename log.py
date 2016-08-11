from datetime import datetime

from models.task import Task
import settings


class Log:

    def update_task(self, task=None):
        if task is not None:
            e_name = input(' Employee Name [{}]: '.format(task.employee))
            if e_name:
                task.employee = e_name
            t_name = input(' Task Name [{}]: '.format(task.name))
            if t_name:
                task.name = t_name

            t_time = input(' Time Spent [{}]: '.format(task.mins))
            if t_time:
                if not Log.valid_num(t_time):
                    t_time = self.prompt_valid_input(
                        'time', ' Time Spent [{}]: '.format(task.mins))
                task.mins = t_time

            date = input(' Task Date [{}]: '.format(task.date))
            if date:
                if not Log.valid_date(date):
                    date = self.prompt_valid_input(
                        'date', ' Task Date [{}]: '.format(task.date))
                task.date = date

            notes = input(' Notes [{}]: '.format(task.notes))
            if notes:
                task.notes = notes

            task.save()

    @staticmethod
    def prompt_verify():
        is_sure = input(' ARE YOU SURE? (Y)/(N): ').lower()
        if is_sure:
            if is_sure[0] == 'y':
                return True
            else:
                return False

    def delete_task(self, task=None):
        if task is not None:
            if Log.prompt_verify():
                task.delete_instance()
                print(' Task Deleted.')
                return True
            else:
                return False
        return False

    def all_tasks(self):
        tasks = self.task.select().order_by(Task.date.desc())
        return tasks

    def add_task(self):
        emp_name = Log.prompt_valid_input('name', 'Employee Name')
        t_name = Log.prompt_valid_input('name', 'Task Name')
        t_time = Log.prompt_valid_input('time', 'Time Spent (in minutes)')
        date = Log.prompt_valid_input('date', 'Task Date')
        notes = Log.prompt_valid_input('notes', 'Notes')
        self.task.create(
            employee=emp_name,
            name=t_name,
            mins=t_time,
            date=date,
            notes=notes
        )

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
            print(' ** Incorrect date format, should be MM/DD/YYYY **')
            return False
        return True

    @staticmethod
    def valid_num(num):
        """Returns True if the input was in-fact an integer."""
        try:
            val = int(num)
        except ValueError:
            print(' Sorry, it needs to be a number.')
            return False
        return True

    @staticmethod
    def valid_name(name=''):
        """Returns True if non-empty string was given."""
        if name:
            return name
        else:
            print(' ** You must enter a name. **')

    @staticmethod
    def prompt_valid_input(method='', prmpt=''):
        if method and prmpt:
            while True:
                usr_input = input(' {}: '.format(prmpt))
                if method == 'name':
                    if Log.valid_name(usr_input):
                        return usr_input
                elif method == 'time':
                    if Log.valid_num(usr_input):
                        return usr_input
                elif method == 'date':
                    if Log.valid_date(usr_input):
                        return usr_input
                elif method == 'notes':
                    return usr_input
                else:
                    break
        return None

    def __init__(self):
        self.db = settings.DB
        self.connect()
        self.task = Task
