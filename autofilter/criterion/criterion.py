from abc import abstractmethod, ABC
from typing import Any, Type, TypeVar
from ast import Call

Query = TypeVar("Query")
Entity = TypeVar("Entity")


class Criterion(ABC):
    @classmethod
    @abstractmethod
    def from_node(cls, node: Any, operators: Any) -> "Criterion":
        ...

    @classmethod
    @abstractmethod
    def match(cls, node: Any) -> Type["Criterion"]:
        ...

    @classmethod
    def determine_type(cls, node: Any, operators) -> Type["Criterion"]:
        for operator in operators:
            if operator.type == node.func.id:
                return operator

    @classmethod
    def init_child(cls, node: Any, operators):
        for operator in operators:
            if operator.match(node, operators):
                kls = operator
                break
        return kls.from_node(node, operators)

    def execute_field(cls, value, *args, **kwargs):
        if isinstance(value, Criterion):
            return value.execute(*args, **kwargs)
        return value

    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        ...

    @classmethod
    def match(cls, node):
        return isinstance(node, Call) and cls.type == node.func.id
