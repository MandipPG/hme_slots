__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

import datetime
from models.slot import Slot
from typing import List, Dict
from commons.helper import parse_time

WEEK_LEN = 7


class SlotFinder(object):

    def get_next_n_slots(self, week_config: List[List[Dict]], current_time: datetime, n=10):
        next_n_slots = []
        week_day = current_time.weekday()
        idx_week = week_day

        while True:
            if idx_week == week_day + WEEK_LEN - 1 and len(next_n_slots) == 0:
                return []
            for slot in map(lambda s: Slot(parse_time(s['start_time']), parse_time(s['end_time'])),
                            week_config[idx_week % WEEK_LEN]):
                if len(next_n_slots) >= n:
                    return [slot.to_dict for slot in next_n_slots]
                slot.make(current_time + datetime.timedelta(days=idx_week - week_day))
                if slot.start >= current_time:
                    next_n_slots.append(slot)
            idx_week += 1
        return [slot.to_dict for slot in next_n_slots]

