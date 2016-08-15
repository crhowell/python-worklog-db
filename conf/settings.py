"""
Application Settings for Python WorkLog w DB

DATE_FORMAT: Is the display format to be used for
display in the terminal when a Task is being shown.

COMPANY_NAME: Used for the company title prompts inside
the application. Also used as reference for database filename.

Ex:
COMPANY_NAME = 'MY_COMPANY'
will look for or create a database file, named 'my_company.db'

"""

import os


# Display Date Format, ex: 2016 Jan 01
DATE_FORMAT = '%Y %b %d'

# Enter your Company's name
COMPANY_NAME = 'MY COMPANY'

# File Location Settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILENAME = COMPANY_NAME.lower().replace(' ', '_') + '.db'

# SQLite Database Location
DB = FILENAME


