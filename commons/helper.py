__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

import importlib
from time import struct_time, strptime
from commons.exceptions import UnsupportedTimeFormatError


def parse_time(time_str: str) -> struct_time:
    """
    Parse the `time_str` and construct `time.struct_time` object.
    :param time_str: Time value
    :return: `time.struct_time` object

    Usage:
    >>> parse_time('06:30')

    """
    time_formats = ('%H:%M', '%H:%M:%S')
    parsed_time: struct_time = None
    for time_format in time_formats:
        try:
            parsed_time = strptime(time_str, time_format)
            break
        except ValueError as ve:
            pass
    if parsed_time is None:
        raise UnsupportedTimeFormatError(time_str)
    return parsed_time


def load_class(fully_qualified_class_name):
    """
    Dynamically loads/imports a class by it's fully qualified name.

    Note - It returns class **type**, NOT the instance of class.

    Usage -
            `my_class = load_class('my_package.my_module.MyClass')`

            `my_class_obj = my_class()`

    """
    class_data = fully_qualified_class_name.split(".")
    module_path = ".".join(class_data[:-1])
    class_str = class_data[-1]

    module = importlib.import_module(module_path)
    return getattr(module, class_str)

def inject(injectable_class, *args, **kwargs):

    """
    :param injectable_class: Either fully qualified name of **injectable_class**.
                                i.e. `my_module.some_pkg.SomeClass` or type(`cls`) of class
    :param args: Arguments required to instantiate **injectable_class**,
                    as defined under `__init__` of **injectable_class**.
    :param kwargs: Keyword args required to instantiate **injectable_class**,
                    as defined under `__init__` of **injectable_class**.
    :return: An instance of **injectable_class**

    Injects the **injectable_class** inside a another class.

    Usage::
        * service_obj = inject('my_package.my_services.MyService', "arg1", "some_arg", kw1="val1")
        * service_obj = inject(MyService, "arg1", "some_arg", kw1="val1")

    """
    if type(injectable_class) == str:
        from commons.helper import load_class
        injectable_class = load_class(injectable_class)
    return injectable_class(*args, **kwargs)