from datetime import datetime
import unittest

from logs import log
from logs.models.task import Task
from peewee import *

TEST_DB = SqliteDatabase(':memory:')
TEST_DB.connect()
TEST_DB.create_tables([Task], safe=True)

TEST_DATA = {
    'employee': 'Test 1',
    'project': 'Project Test',
    'name': 'Task 1',
    'mins': 2,
    'date': '01/02/2016',
    'notes': 'Test Data 1'
}


class LogTests(unittest.TestCase):

    def setUp(self):
        self.log = log.Log()
        self.test_task = self.log.add_task(TEST_DATA)

    def test_task_delete(self):
        task_id = self.test_task.id
        task = self.log.delete_task(task_id)
        self.assertTrue(task)

    def test_task_delete_not_found(self):
        task = self.log.delete_task('0')
        self.assertFalse(task)

    def test_bad_task_delete(self):
        task = self.log.delete_task(None)
        self.assertFalse(task)

    def test_task_update(self):
        task_id = self.test_task.id
        data = TEST_DATA
        data['mins'] = 2
        edits = self.log.update_task(task_id, data)
        self.assertTrue(edits)

    def test_bad_task_update(self):
        edits = self.log.update_task({})
        self.assertFalse(edits)

    def test_bad_task_add(self):
        task = self.log.add_task({})
        self.assertFalse(task)

    def test_find_by_employee(self):
        task = self.log.find_task('employee', 'Test 1')
        self.assertTrue(task)

    def test_find_by_date_range(self):
        task = self.log.find_task('rdate', ['01/01/2016', '01/03/2016'])
        self.assertTrue(task)

    def test_find_by_mins_range(self):
        task = self.log.find_task('rtime', [1, 3])

    def test_find_by_exact_date(self):
        task = self.log.find_task('date', '01/02/2016')
        self.assertTrue(task)

    def test_find_by_project_name(self):
        task = self.log.find_task('project', 'project_test')
        self.assertTrue(task)

    def test_bad_find_by(self):
        task = self.log.find_task('not here', 'oops')
        self.assertFalse(task)

    def test_bad_find_task(self):
        task = self.log.find_task(None, '')
        self.assertFalse(task)

    def test_invalid_num(self):
        num = self.log.valid_num('three')
        self.assertFalse(num)

    def test_valid_num(self):
        num = self.log.valid_num(3)
        self.assertTrue(num)

    def test_invalid_name(self):
        name = self.log.valid_name('')
        self.assertFalse(name)

    def test_valid_name(self):
        name = self.log.valid_name('Peter Griffin')
        self.assertTrue(name)

    def test_invalid_date_format(self):
        date = self.log.valid_date('2016/01/01')
        self.assertFalse(date)

    def test_valid_date_format(self):
        date = self.log.valid_date('01/01/2016')
        self.assertTrue(date)

    def test_bad_date_conversion(self):
        date = self.log.convert_date('01/01/2016', '%Y/%m/%d')
        self.assertFalse(date)

    def test_date_conversion(self):
        date = self.log.convert_date('01/01/2016')
        self.assertIsInstance(date, datetime)

    def tearDown(self):
        self.test_task.delete_instance()


if __name__ == '__main__':
    unittest.main()

