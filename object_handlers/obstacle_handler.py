from objects import Obstacle, Object
from data_containers import objects as obj_container
from .object_handler import ObjectHandler


class ObstacleHandler(ObjectHandler):
    @classmethod
    def update(cls, obj: Obstacle) -> None:
        if cls.delete_if_passed_camera(obj):
            return

        # TODO Logis for skeleton:
        # ... physics
        # ... update invisibility time