import sys
from datetime import datetime

from conf import settings
from .log import Log


class WorkLog:

    def main(self):
        self.clear_screen()
        while True:
            print("\n {}'s WorkLog\n".format(settings.COMPANY_NAME))
            choices = self.display_main_menu()
            menu_choice = self.prompt_menu_choice(choices)
            self.get_main_selection(menu_choice)
            self.clear_screen()

    def edit_task(self, task=None):
        if task is not None:
            print('\n * Leave blank to keep field unchanged. *')
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

            data = {
                'id': task.id,
                'edits': {
                    'employee': task.employee,
                    'name': task.name,
                    'mins': task.mins,
                    'date': task.date,
                    'notes': task.notes}
                }
            self.log.update_task(data)

    def display_find_menu(self):
        """Display to terminal, the Find sub-menu"""
        self.clear_screen()
        print('\n Find By...')
        print('{}{}'.format(' ', '-' * 45))
        print('{}\n{}\n{}\n{}\n{}\n{}\n{}\n'.format(
            ' (E)mployee Name',
            ' (L)ist of Dates',
            ' (R)ange of Dates',
            ' (T)ime spent (range)',
            ' (S)earch term',
            ' (P)roject related',
            ' (Q)uit menu'
        ))
        return ['e', 'l', 'r', 't', 's', 'p', 'q']

    def display_paginated(self, tasks=[]):
        if tasks:
            i = 0
            while True:
                self.clear_screen()
                page_dir = self.allowable_page_dir(i, len(tasks))
                choices = [key for key in page_dir]
                self.display_task_count(i+1, len(tasks))
                self.display_task(tasks[i])
                prompt = ' | '.join([page_dir[key] for key in choices])
                choice = self.prompt_menu_choice(choices, '[{}]: '.format(prompt))
                if choice == 'p':
                    i -= 1
                elif choice == 'n':
                    i += 1
                elif choice == 'e':
                    self.edit_task(tasks[i])
                    self.prompt_action_status(' Task updated.')
                    break
                elif choice == 'd':
                    is_deleted = self.log.delete_task(tasks[i])
                    if is_deleted:
                        self.prompt_action_status(' Task deleted.')
                    else:
                        self.prompt_action_status(' Task NOT deleted.')
                    break
                elif choice == 'q':
                    break

    def prompt_find_choice(self, choice=''):
        result = None
        if choice:
            while True:
                if choice == 'e':
                    # Find by employee
                    print(' Search by Employee Name ')
                    name = input(' Employee Name: ')
                    if name:
                        result = self.log.find_task('employee', name)
                        break
                    else:
                        print(' ** You must enter a name to search for. ** ')
                        continue
                elif choice == 'l':
                    pass
                elif choice == 'r':
                    # Find by Range Dates
                    print(' Date format is: mm/dd/yyyy')
                    date1 = self.prompt_valid_input('date', 'First Date (older)')
                    date2 = self.prompt_valid_input('date', 'Recent Date (recent)')
                    result = self.log.find_task('rdate', [date1, date2])
                    break
                elif choice == 't':
                    # Find by Time Spent
                    min_time = input('\n Enter MINimum time (in minutes): ')
                    if self.log.valid_num(min_time):
                        max_time = input(' \n Enter MAXimum time (in minutes): ')
                        if self.log.valid_num(max_time):
                            result = self.log.find_task('rtime', [min_time, max_time])
                            break
                        else:
                            print('\n ** Please enter a valid MAX time.')
                    else:
                        print('\n ** Please enter a valid MIN time.')
                # Find by Search Term
                elif choice == 's':
                    pass
                # Find by Project Name
                elif choice == 'p':
                    pass
                elif choice == 'q':
                    break
        else:
            return False

        return result

    def get_main_selection(self, choice=''):
        if choice:
            if choice == 'a':
                task = self.prompt_task()
                self.log.add_task(task)
                self.prompt_action_status('Task Added')
                self.clear_screen()
            elif choice == 'f':
                choices = self.display_find_menu()
                choice = self.prompt_menu_choice(choices)
                search = self.prompt_find_choice(choice)
                if search:
                    self.display_paginated(search)
                else:
                    self.prompt_action_status('No results found.')

            elif choice == 'q':
                self.clear_screen()
                print('\n Exiting...')
                print("\n Thanks for using {}'s Worklog".format(
                    settings.COMPANY_NAME
                ))
                print(' Have a great day!')
                sys.exit(0)

    @staticmethod
    def prompt_verify():
        is_sure = input(' ARE YOU SURE? (Y)/(N): ').lower()
        if is_sure:
            if is_sure[0] == 'y':
                return True
            else:
                return False

    @staticmethod
    def prompt_valid_input(method='', prmpt=''):
        if method and prmpt:
            while True:
                usr_input = input(' {}: '.format(prmpt))
                if method == 'name':
                    if Log.valid_name(usr_input):
                        return usr_input
                    else:
                        print(' ** Cannot be an empty name, try again. **')
                elif method == 'time':
                    if Log.valid_num(usr_input):
                        return usr_input
                    else:
                        print(' ** You must enter total minutes(number), ' +
                              'try again. **')
                elif method == 'date':
                    if Log.valid_date(usr_input):
                        return usr_input
                    else:
                        print(' ** You must enter a valid date MM/DD/YYYY, ' +
                              'try again. **')
                elif method == 'notes':
                    return usr_input
                else:
                    break
        return None

    def prompt_task(self):
        emp_name = self.prompt_valid_input('name', 'Employee Name')
        t_name = self.prompt_valid_input('name', 'Task Name')
        t_time = self.prompt_valid_input('time', 'Time Spent (in minutes)')
        date = self.prompt_valid_input('date', 'Task Date')
        notes = self.prompt_valid_input('notes', 'Notes')
        return {
            'employee': emp_name,
            'name': t_name,
            'mins': t_time,
            'date': date,
            'notes': notes
        }

    @staticmethod
    def prompt_action_status(prompt='\n'):
        input('\n {}. Press ENTER to continue.'.format(prompt))

    @staticmethod
    def prompt_menu_choice(choices=[], prompt=' Choice: '):
        """Prompts and validates a choice,
        based-on list of valid choices.

        Keyword arguments:
        choices -- list of valid choices
        prompt -- prompt to be displayed
        """
        while True:
            choice = input(' {} '.format(prompt)).lower()
            if choice:
                if choice[0] in choices:
                    return choice[0]
                else:
                    print('\n Try again, that was not a valid choice.')
            else:
                print('\n Try again, you must enter a choice.')

    @staticmethod
    def display_verify():
        print(' ** ARE YOU SURE? (Y)/(N)')
        return ['y', 'n']

    @staticmethod
    def display_task_count(curr=None, count=None):
        """Displays to terminal
        task number and total number of tasks.

        Keyword arguments:
        curr -- current number
        count -- count of tasks
        """
        if curr is not None and count is not None:
            print('\n Task {} of {}\n'.format(curr, count))

    @staticmethod
    def display_task(task=None):
        if task is not None:
            print('=' * 45)
            print(' Task Name: {}'.format(task.name))
            print(' Employee: {}'.format(task.employee))
            print(' Date: {}'.format(task.date))
            print(' Time Spent: {}'.format(task.mins))
            print(' Notes: {}'.format(task.notes))
            print('=' * 45)

    @staticmethod
    def display_main_menu():
        """Displays to terminal the Main Menu selections."""
        print(' What would you like to do? ')
        print('{}{}'.format(' ', '-' * 45))
        print('{}\n{}\n{}\n'.format(
            ' A)dd Task',
            ' F)ind A Task',
            ' Q)uit Application'
        ))
        return ['a', 'f', 'q']

    @staticmethod
    def clear_screen():
        """Clears the terminal screen"""
        print('\033c', end='')

    @staticmethod
    def convert_display_date(date, fmt='%m/%d/%Y'):
        """Converts a date to settings DATE_DISPLAY_FORMAT

        Keyword arguments:
        date -- user input date
        fmt -- format of input date
        """
        return datetime.strptime(date, fmt).strftime(
            settings.DATE_FORMAT)

    @staticmethod
    def allowable_page_dir(num, size):
        """Returns list of allowable pagination directions.

        Keyword arguments:
        num -- Current task number
        size -- Size of the list of tasks
        """
        choices = {
            'e': '(E)dit',
            'd': '(D)elete',
            'p': '(P)revious',
            'n': '(N)ext',
            'q': '(Q)uit'
        }
        if 0 < num < size - 1:
            return choices
        elif num == 0:
            del choices['p']
            if num == size - 1:
                del choices['n']
            return choices
        else:
            del choices['n']
            return choices

    def __init__(self):
        self.log = Log()
