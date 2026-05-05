from objects import Allosaurus, Poo, Object
from object_handlers.object_handler import ObjectHandler
from data_containers import objects as obj_container


class PooHandler(ObjectHandler):
    @classmethod
    def update(cls, obj: Poo) -> None:
        pass