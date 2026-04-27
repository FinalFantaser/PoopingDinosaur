from data_containers import objects as obj_container
from objects import *


class ObjectHandler:
    @classmethod
    def update(cls, obj: Object|str) -> Object:
        if isinstance(obj, str):
            return obj_container.get(obj, True)
        else:
            return obj

    @classmethod
    def read_input(cls, obj: Object|str) -> None:
        pass