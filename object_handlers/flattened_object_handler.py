from pygame.time import get_ticks

from objects.flattened_object import FlattenedObject
from .object_handler import ObjectHandler
from data_containers import objects as obj_container


class FlattenedObjectHandler(ObjectHandler):
    @classmethod
    def update(cls, obj: FlattenedObject) -> None:
        if get_ticks() - obj.created_at >= obj.LIFETIME:
            obj_container.queue_delete(obj)
            return

        cls.physics(obj)