__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

from datetime import datetime
from time import strptime, struct_time
import json
from commons.exceptions import InvalidSlotError

class Slot(object):
    """
    Represents a slot.
    """
    def __init__(self, start_time: struct_time, end_time: struct_time):
        self.__start_time__ = start_time
        self.__end_time__ = end_time

        if not self.is_valid:
            raise InvalidSlotError(start_time, end_time)

        self.start: datetime = None
        self.end: datetime = None

    def make(self, current_time: datetime):
        """
        Attach the date information to time information in order to mark the slot as `Assigned`. e.g.
        
        self.start = start_date + self.__start_time
        self.end = end_date + self.__end_time
        
        """
        self.start = datetime(year=current_time.year,month=current_time.month, day=current_time.day,
                                hour=self.__start_time__.tm_hour, minute=self.__start_time__.tm_min,
                                second=self.__start_time__.tm_sec)
        self.end = datetime(year=current_time.year, month=current_time.month, day=current_time.day,
                                hour=self.__end_time__.tm_hour, minute=self.__end_time__.tm_min,
                                second=self.__end_time__.tm_sec)

    @property
    def is_valid(self):
        """
        Checks if slot is valid or not. If slot duration is more than 24 hours then slot is considered as invalid.
        """
        return self.__end_time__ > self.__start_time__

    @property
    def to_dict(self):
        """
        Converts the underlying slot to dictionary so that it can be serialized/deserialized later, if required.
        """
        return {
            'start_time': self.start.strftime('%Y-%m-%d %H:%M:%S'),
            'end_time': self.end.strftime('%Y-%m-%d %H:%M:%S')
        }

    @property
    def __key__(self):
        return self.start, self.end

    def __str__(self):
        return json.dumps(self.to_dict)

    def __hash__(self):
        return hash(self.__key__)

    def __eq__(self, other):
        return self.__key__ == other.__key__
