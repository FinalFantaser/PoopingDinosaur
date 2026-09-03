from pygame.time import get_ticks
from objects import Object, Obstacle, TRexNew, Allosaurus, FlattenedObject
from .object_handler import ObjectHandler
from .dinosaur_handler import DinosaurHandler
from data_containers import objects as obj_container, game_data


class AllosaurusHandler(ObjectHandler):
    @classmethod
    def update(cls, obj: Allosaurus) -> None:
        if cls.delete_if_passed_camera(obj):
            return

        cls.physics(obj)

        # ...

        obj.last_update = get_ticks()