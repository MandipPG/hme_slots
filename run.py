__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

from pprint import pprint
import datetime
from services.slot_finder import SlotFinder
from commons.helper import inject

INP_1 = [[]] * 7
INP_2 = [
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
INP_3 = [
    [  # Monday

    ],
    [  # Tuesday

    ],
    [],  # Wednesday
    [
        {"start_time": "09:00", "end_time": "10:00"}
    ],
    [], # Friday
    [], # Saturday
    [],  # Sunday
]


if __name__ == '__main__':
    slot_finder = inject(SlotFinder)
    current_time = datetime.datetime(2017, 1, 3, 7, 0, 0)  # Tuesday, weekday = 1
    # current_time = datetime.datetime(2017, 1, 4, 7, 0)  # Wed, weekday = 2
    # current_time = datetime.datetime(2017, 1, 3, 7, 20)  # Tuesday, weekday = 1
    next_n_slots = slot_finder.get_next_n_slots(INP_3, current_time)
    pprint(next_n_slots)


