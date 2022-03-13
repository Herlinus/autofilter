from typing import Any, List
from .criterion import Criterion
from . import is_operator


class Expression(Criterion):
    type: str
    criteria: List[Criterion]

    def __init__(self, *criteria):
        self.criteria = criteria

    @classmethod
    def from_node(cls, node, operators):
        criteria = [cls.init_child(arg, operators) for arg in node.args]
        return cls(*criteria)


@is_operator
class AndExpression(Expression):
    type = "And"

    def execute(self, *args, **kwargs) -> Any:
        return all(criterion.execute(*args, **kwargs) for criterion in self.criteria)


@is_operator
class OrExpression(Expression):
    type = "Or"

    def execute(self, *args, **kwargs) -> Any:
        return any(criterion.execute(*args, **kwargs) for criterion in self.criteria)


@is_operator
class NotExpression(Expression):
    type = "Not"
    criterion: Criterion

    def __init__(self, criterion):
        self.criterion = criterion

    @classmethod
    def from_node(cls, node, operators):
        criterion = cls.init_child(node.args[0], operators)
        return cls(criterion)

    def execute(self, *args, **kwargs) -> Any:
        return not self.criterion.execute(*args, **kwargs)
