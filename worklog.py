from datetime import datetime

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
                    # TODO
                    print('edit placeholder...')
                    break
                elif choice == 'd':
                    # TODO
                    print('delete placeholder...')
                    break
                elif choice == 'q':
                    break

    def get_main_selection(self, choice=''):
        if choice:
            if choice == 'a':
                self.log.add_task()
                self.prompt_action_status('Task Added')
                self.clear_screen()
            elif choice == 'f':
                tasks = self.log.all_tasks()
                self.display_paginated(tasks)

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
            print(' Task Name: {}\n Minutes Spent: {}\n Notes: {}\n Date: {}'.format(
                task.name,
                task.mins,
                task.notes,
                task.date
            ))
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
