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


