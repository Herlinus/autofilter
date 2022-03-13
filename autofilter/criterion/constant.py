from ast import Constant, Name, Attribute
from typing import Any

from .criterion import Criterion
from . import is_operator


@is_operator
class CriterionConstant(Criterion):
    value: str

    def __init__(self, value) -> None:
        self.value = value

    @classmethod
    def match(cls, node):
        return isinstance(node, Constant)

    @classmethod
    def from_node(cls, node: Any, operators: Any):
        return cls(node.value)

    def execute(self, *args, **kwargs) -> Any:
        return self.value


@is_operator
class AttributeAcesser(CriterionConstant):
    @classmethod
    def get_path(cls, node, current_leaf=None):
        current_leaf = current_leaf or []
        if isinstance(node, Name):
            return [node.id] + current_leaf
        return cls.get_path(node.value, [node.attr] + current_leaf)

    @classmethod
    def from_node(cls, node: Any, operators: Any):
        path = cls.get_path(node)
        return cls(".".join(path))

    @classmethod
    def match(cls, node):
        return isinstance(node, (Name, Attribute))

    def execute(self, *args, **kwargs) -> Any:
        return self.value
