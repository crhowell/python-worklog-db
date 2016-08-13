from datetime import datetime
import sys

from log import Log
import settings


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
            self.log.update_task(task)

    def display_find_menu(self):
        """Display to terminal, the Find sub-menu"""
        self.clear_screen()
        print('\n Find By...')
        print('{}{}'.format(' ', '-' * 45))
        print('{}\n{}\n{}\n{}\n{}\n{}\n'.format(
            ' (E)mployee Name',
            ' (L)ist of Dates'
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
                    self.log.update_task(tasks[i])
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
                date1 = self.log.prompt_valid_input('date', 'First Date (older)')
                date2 = self.log.prompt_valid_input('date', 'Recent Date (recent)')
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

        return result

    def get_main_selection(self, choice=''):
        if choice:
            if choice == 'a':
                self.log.add_task()
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

                # if tasks:
                #     self.display_paginated(tasks)
                # else:
                #     self.prompt_action_status(' There are no entries.')
            elif choice == 'q':
                self.clear_screen()
                print('\n Exiting...')
                print("\n Thanks for using {}'s Worklog".format(
                    settings.COMPANY_NAME
                ))
                print(' Have a great day!')
                sys.exit(0)

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
