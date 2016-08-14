from datetime import datetime
import unittest

from logs import log


class LogTests(unittest.TestCase):

    def setUp(self):
        self.log = log.Log()

    def test_bad_task_delete(self):
        task = self.log.delete_task(None)
        self.assertFalse(task)

    def test_bad_task_update(self):
        edits = self.log.update_task({})
        self.assertFalse(edits)

    def test_bad_task_add(self):
        task = self.log.add_task({})
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

if __name__ == '__main__':
    unittest.main()
