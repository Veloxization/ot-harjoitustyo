import unittest
import datetime
from classes.time import Time

class TestTime(unittest.TestCase):
    def setUp(self):
        self.time = Time(36)
        self.index = 9
        self.string = "19:30"
        self.wanted_time = datetime.datetime(1900,1,1,hour=19, minute=30)

    def test_final_time_is_set_correctly(self):
        test_time = Time(3)
        self.assertEqual(test_time.final_time, datetime.datetime(1900,1,1,hour=18, minute=30))
        test_time = Time(7)
        self.assertEqual(test_time.final_time, datetime.datetime(1900,1,1,hour=19, minute=10))

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

    def test_index_to_time_returns_final_time_with_large_index(self):
        result_time = self.time.index_to_time(9999999)
        self.assertEqual(result_time, datetime.datetime(1900,1,2))

    def test_time_to_index_returns_final_time_with_later_time(self):
        result_index = self.time.time_to_index(datetime.datetime(2000,1,1))
        self.assertEqual(result_index, 36)

    def test_string_to_time_returns_none_with_incompatible_string(self):
        result_time = self.time.string_to_time("TEST")
        self.assertEqual(result_time, None)

    def test_string_to_index_returns_none_with_incompatible_string(self):
        result_index = self.time.string_to_index("TEST")
        self.assertEqual(result_index, None)

    def test_negative_index_in_index_to_time_returns_start_time(self):
        result_time = self.time.index_to_time(-1)
        self.assertEqual(result_time, datetime.datetime(1900,1,1,hour=18))

    def test_time_before_start_time_converted_to_next_day_in_string_to_time(self):
        result_time = self.time.string_to_time("17:59")
        self.assertEqual(result_time, datetime.datetime(1900,1,2,hour=17,minute=59))
