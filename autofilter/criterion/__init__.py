OPERATORS = []


def is_operator(cls):
    OPERATORS.append(cls)
    return cls


from .operator import *
from .constant import *
from .expression import *
