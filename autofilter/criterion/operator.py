import re
from typing import Any
from .criterion import Criterion
from . import is_operator


class Operator(Criterion):
    field: Criterion
    value: Criterion
    type: str

    @classmethod
    def from_node(cls, node, operators):
        field = cls.init_child(node.args[0], operators)
        value = cls.init_child(node.args[1], operators)
        return cls(field, value)

    def __init__(self, field, value):
        self.field = field
        self.value = value

    def execute(self, *args, **kwargs) -> Any:
        field = self.field.execute(*args, **kwargs)
        value = self.value.execute(*args, **kwargs)
        return self._execute(field, value)


@is_operator
class Equal(Operator):
    type = "Eq"

    def _execute(self, field, value, *args, **kwargs):
        return field == value


@is_operator
class LowerThan(Operator):
    type = "Lt"

    def _execute(self, field, value, *args, **kwargs):
        return field < value


@is_operator
class LowerThanOrEq(Operator):
    type = "Lte"

    def _execute(self, field, value, *args, **kwargs):
        return field <= value


@is_operator
class GreaterThan(Operator):
    type = "Gt"

    def _execute(self, field, value, *args, **kwargs):
        return field > value


@is_operator
class GreaterThan(Operator):
    type = "Gte"

    def _execute(self, field, value, *args, **kwargs):
        return field >= value


@is_operator
class Like(Operator):
    type = "Like"

    def _execute(self, field, value: str, *args, **kwargs):
        return field.__like__(value)


@is_operator
class Between(Criterion):
    type = "Btw"

    def __init__(self, field, left_value, right_value):
        self.field = field
        self.left_value = left_value
        self.right_value = right_value

    @classmethod
    def from_node(cls, node, operators):
        field = cls.init_child(node.args[0], operators)
        left_value = cls.init_child(node.args[1], operators)
        right_value = cls.init_child(node.args[2], operators)
        return cls(field, left_value, right_value)

    def execute(self, *args, **kwargs) -> Any:
        field = self.field.execute(*args, **kwargs)
        left_value = self.left_value.execute(*args, **kwargs)
        right_value = self.right_value.execute(*args, **kwargs)
        return self._execute(field, left_value, right_value, *args, **kwargs)

    def _execute(self, field, left_value, right_value, *args, **kwargs):
        return left_value <= field <= right_value
