__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

from time import struct_time

class InvalidSlotError(Exception):
    def __init__(self, start_time: struct_time, end_time: struct_time):
        start_time_str = '{}:{}:{}'.format(start_time.tm_hour, start_time.tm_min, start_time.tm_sec)
        end_time_str = '{}:{}:{}'.format(end_time.tm_hour, end_time.tm_min, end_time.tm_sec)
        message = "Invalid time slot({} - {})".format(start_time_str, end_time_str)

        super(InvalidSlotError, self).__init__(message)
        self.start_time = start_time
        self.end_time = end_time

class UnsupportedTimeFormatError(ValueError):
    def __init__(self, time_str):
        message = "Couldn't parse the value {}".format(time_str)
        super(UnsupportedTimeFormatError, self).__init__(message)

