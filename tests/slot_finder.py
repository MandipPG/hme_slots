__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

import unittest
import datetime
from services.slot_finder import SlotFinder
from commons.exceptions import UnsupportedTimeFormatError, InvalidSlotError
from commons.helper import inject

class TestSlotFinder(unittest.TestCase):

    def setUp(self):
        self.slot_finder = inject(SlotFinder)

    def tearDown(self):
        self.slot_finder = None

    def test_1_invalid_slot(self):
        """
        Invalid time slot: stat_time > end_time.
        If start_time is > end_time then it means that slot duration is more than 24 hours.
        :return:
        """
        week_config = [
            [],
            [],
            [],
            [
                {"start_time": "05:00", "end_time": "04:00"}
            ],
            [],
            [],
            [],
        ]
        time_of_run = datetime.datetime(2017, 1, 3, 7, 0)  # Tuesday, weekday = 1
        self.assertRaises(InvalidSlotError, self.slot_finder.get_next_n_slots, week_config, time_of_run)

    def test_2_unsupported_time_format(self):
        """
        `05:30:25.12` contains milliseconds, which is not supported.
        :return:
        """
        week_config = [
            [],
            [],
            [],
            [
                {"start_time": "05:30:25.12", "end_time": "08:00"}
            ],
            [],
            [],
            [],
        ]
        time_of_run = datetime.datetime(2017, 1, 3, 7, 0)  # Tuesday, weekday = 1
        self.assertRaises(UnsupportedTimeFormatError, self.slot_finder.get_next_n_slots, week_config, time_of_run)

    def test_3_time_format_without_seconds(self):
        """
        All the slot time values contains `hour` & `minutes` information only.
        :return:
        """
        week_config = [
            [  # Monday
                {"start_time": "06:00", "end_time": "06:30"},
                {"start_time": "06:30", "end_time": "07:00"},
                {"start_time": "07:00", "end_time": "07:30"},
                {"start_time": "07:30", "end_time": "08:00"}
            ], [  # Tuesday
            ], [  # Wednesday
                {"start_time": "06:00", "end_time": "06:30"},
                {"start_time": "06:30", "end_time": "07:00"},
                {"start_time": "07:00", "end_time": "07:30"},
                {"start_time": "07:30", "end_time": "08:00"}
            ], [  # Thursday
                {"start_time": "09:00", "end_time": "09:30"},
                {"start_time": "09:30", "end_time": "10:00"},
                {"start_time": "10:00", "end_time": "10:30"},
                {"start_time": "10:30", "end_time": "11:00"}
            ], [  # Friday
            ], [  # Saturday
            ], [  # Sunday
            ]
        ]

        expected_output = [
            {"start_time": "2017-01-02 06:00:00", "end_time": "2017-01-02 06:30:00"},
            {"start_time": "2017-01-02 06:30:00", "end_time": "2017-01-02 07:00:00"},
            {"start_time": "2017-01-02 07:00:00", "end_time": "2017-01-02 07:30:00"},
            {"start_time": "2017-01-02 07:30:00", "end_time": "2017-01-02 08:00:00"},
            {"start_time": "2017-01-04 06:00:00", "end_time": "2017-01-04 06:30:00"},
            {"start_time": "2017-01-04 06:30:00", "end_time": "2017-01-04 07:00:00"},
            {"start_time": "2017-01-04 07:00:00", "end_time": "2017-01-04 07:30:00"},
            {"start_time": "2017-01-04 07:30:00", "end_time": "2017-01-04 08:00:00"},
            {"start_time": "2017-01-05 09:00:00", "end_time": "2017-01-05 09:30:00"},
            {"start_time": "2017-01-05 09:30:00", "end_time": "2017-01-05 10:00:00"}
        ]
        time_of_run = datetime.datetime(2017, 1, 1, 20, 30)  # Sunday
        next_n_slots = self.slot_finder.get_next_n_slots(week_config, time_of_run)
        self.assertEqual(next_n_slots, expected_output)

    def test_4_time_format_with_seconds(self):
        """
        Slot time values can also contains the `seconds` information.
        :return:
        """
        week_config = [
            [  # Monday
                {"start_time": "06:00:30", "end_time": "06:30"},
                {"start_time": "06:30", "end_time": "07:00:20"},
            ],
            [  # Tuesday
                {"start_time": "06:00", "end_time": "06:30:20"},
                {"start_time": "07:00:45", "end_time": "07:30"},
                {"start_time": "07:30:20", "end_time": "07:45:40"}
            ],
            [],  # Wednesday
            [
                {"start_time": "09:00", "end_time": "10:00"}
            ],
            [], # Friday
            [], # Saturday
            [],  # Sunday
        ]
        expected_output = [{'end_time': '2017-01-03 07:30:00', 'start_time': '2017-01-03 07:00:45'},
             {'end_time': '2017-01-03 07:45:40', 'start_time': '2017-01-03 07:30:20'},
             {'end_time': '2017-01-05 10:00:00', 'start_time': '2017-01-05 09:00:00'},
             {'end_time': '2017-01-09 06:30:00', 'start_time': '2017-01-09 06:00:30'},
             {'end_time': '2017-01-09 07:00:20', 'start_time': '2017-01-09 06:30:00'},
             {'end_time': '2017-01-10 06:30:20', 'start_time': '2017-01-10 06:00:00'},
             {'end_time': '2017-01-10 07:30:00', 'start_time': '2017-01-10 07:00:45'},
             {'end_time': '2017-01-10 07:45:40', 'start_time': '2017-01-10 07:30:20'},
             {'end_time': '2017-01-12 10:00:00', 'start_time': '2017-01-12 09:00:00'},
             {'end_time': '2017-01-16 06:30:00', 'start_time': '2017-01-16 06:00:30'}
        ]
        time_of_run = datetime.datetime(2017, 1, 3, 7, 0, 20)
        next_n_slots = self.slot_finder.get_next_n_slots(week_config, time_of_run)
        self.assertEqual(next_n_slots, expected_output)

    def test_5_no_slots(self):
        """
        No slot(s) are available.
        :return:
        """
        week_config = [[]] * 7
        expected_output = []
        current_time = datetime.datetime(2017, 1, 3, 7, 0, 20)
        next_n_slots = self.slot_finder.get_next_n_slots(week_config, current_time)
        self.assertEqual(next_n_slots, expected_output)

    def test_6_circular_slots(self):
        week_config = [
            [  # Monday
                {"start_time": "06:00", "end_time": "06:30"},
                {"start_time": "06:30", "end_time": "07:00"},
            ], [  # Tuesday
                {"start_time": "06:00", "end_time": "06:30"},
                {"start_time": "07:00", "end_time": "07:30"},
                {"start_time": "07:30", "end_time": "07:45"}
            ], [  # Wednesday
            ], [  # Thursday
                {"start_time": "09:00", "end_time": "10:00"}
            ], [  # Friday
            ], [  # Saturday
            ], [  # Sunday
            ]
        ]

        expected_output = [
            {"start_time": "2017-01-02 06:00:00", "end_time": "2017-01-02 06:30:00"},
            {"start_time": "2017-01-02 06:30:00", "end_time": "2017-01-02 07:00:00"},
            {"start_time": "2017-01-03 06:00:00", "end_time": "2017-01-03 06:30:00"},
            {"start_time": "2017-01-03 07:00:00", "end_time": "2017-01-03 07:30:00"},
            {"start_time": "2017-01-03 07:30:00", "end_time": "2017-01-03 07:45:00"},
            {"start_time": "2017-01-05 09:00:00", "end_time": "2017-01-05 10:00:00"},
            {"start_time": "2017-01-09 06:00:00", "end_time": "2017-01-09 06:30:00"},
            {"start_time": "2017-01-09 06:30:00", "end_time": "2017-01-09 07:00:00"},
            {"start_time": "2017-01-10 06:00:00", "end_time": "2017-01-10 06:30:00"},
            {"start_time": "2017-01-10 07:00:00", "end_time": "2017-01-10 07:30:00"}
        ]
        current_time = datetime.datetime(2017, 1, 1, 20, 30)  # Sunday
        next_n_slots = self.slot_finder.get_next_n_slots(week_config, current_time)
        self.assertEqual(next_n_slots, expected_output)

    def test_7_single_slot(self):
        """
        Only one slot is available throughout the week.
        :return:
        """
        week_config = [
            [  # Monday

            ],
            [  # Tuesday

            ],
            [],  # Wednesday
            [
                {"start_time": "09:00", "end_time": "10:00"}
            ],
            [],  # Friday
            [],  # Saturday
            [],  # Sunday
        ]
        expected_output = [{'end_time': '2017-01-05 10:00:00', 'start_time': '2017-01-05 09:00:00'},
             {'end_time': '2017-01-12 10:00:00', 'start_time': '2017-01-12 09:00:00'},
             {'end_time': '2017-01-19 10:00:00', 'start_time': '2017-01-19 09:00:00'},
             {'end_time': '2017-01-26 10:00:00', 'start_time': '2017-01-26 09:00:00'},
             {'end_time': '2017-02-02 10:00:00', 'start_time': '2017-02-02 09:00:00'},
             {'end_time': '2017-02-09 10:00:00', 'start_time': '2017-02-09 09:00:00'},
             {'end_time': '2017-02-16 10:00:00', 'start_time': '2017-02-16 09:00:00'},
             {'end_time': '2017-02-23 10:00:00', 'start_time': '2017-02-23 09:00:00'},
             {'end_time': '2017-03-02 10:00:00', 'start_time': '2017-03-02 09:00:00'},
             {'end_time': '2017-03-09 10:00:00', 'start_time': '2017-03-09 09:00:00'}
        ]
        time_of_run = datetime.datetime(2017, 1, 3, 7, 0, 0)
        next_n_slots = self.slot_finder.get_next_n_slots(week_config, time_of_run)
        self.assertEqual(next_n_slots, expected_output)

if __name__ == '__main__':
    unittest.main()
    # python -m unittest discover -s 'tests' -p '*.py'