from typing import Any, List
from .criterion import Criterion
from ast import parse
from abc import ABC, abstractmethod
from .criterion import OPERATORS


class QueryFilter(ABC):
    @property
    @abstractmethod
    def operators(self):
        pass

    criterion: Criterion

    def __init__(self, criterion: Criterion):
        self.criterion = criterion

    def execute(self, *args, **kwargs):
        if self.criterion:
            return self.criterion.execute(*args, **kwargs)

    @classmethod
    def from_str(cls, value: str) -> Criterion:
        criterion = None
        if value:
            node = parse(value).body[0].value
            criterion = Criterion.init_child(node, cls.operators)
        return cls(criterion)


class BoolQueryFilter(QueryFilter):
    operators = OPERATORS["bool"]
