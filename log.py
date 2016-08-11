from datetime import datetime

from models.task import Task
import settings


class Log:

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
        return None

    def __init__(self):
        self.db = settings.DB
        self.connect()
        self.task = Task
