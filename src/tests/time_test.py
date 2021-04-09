import unittest
import datetime
from classes.time import Time

class TestTime(unittest.TestCase):
    def setUp(self):
        self.time = Time(datetime.datetime(1900,1,2,hour=0, minute=0))
        self.index = 9
        self.string = "19:30"
        self.wanted_time = datetime.datetime(1900,1,1,hour=19, minute=30)

    def test_final_index_is_set_correctly(self):
        test_time = Time(datetime.datetime(1900,1,1,hour=18, minute=30))
        self.assertEqual(test_time.final_index, 3)
        test_time = Time(datetime.datetime(1900,1,1,hour=19, minute=10))
        self.assertEqual(test_time.final_index, 7)

    def test_index_to_time_works_correctly(self):
        result_time = self.time.index_to_time(9)
        self.assertEqual(self.wanted_time, result_time)

    def test_time_to_index_works_correctly(self):
        result_index = self.time.time_to_index(datetime.datetime(1900,1,1,hour=19, minute=30))
        self.assertEqual(self.index, result_index)

    def test_index_to_string_works_correctly(self):
        result_string = self.time.index_to_string(9)
        self.assertEqual(self.string, result_string)

    def test_string_to_index_works_correctly(self):
        resut_index = self.time.string_to_index("19:30")
        self.assertEqual(self.index, resut_index)

    def test_time_to_string_works_correctly(self):
        result_string = self.time.time_to_string(datetime.datetime(1900,1,1,hour=19, minute=30))
        self.assertEqual(self.string, result_string)

    def test_string_to_time_works_correctly(self):
        result_time = self.time.string_to_time("19:30")
        self.assertEqual(self.wanted_time, result_time)
