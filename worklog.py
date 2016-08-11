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

    def get_main_selection(self, choice=''):
        if choice:
            if choice == 'a':
                self.log.add_task()
                self.prompt_action_status('Task Added')
                self.clear_screen()

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

    def __init__(self):
        self.log = Log()
