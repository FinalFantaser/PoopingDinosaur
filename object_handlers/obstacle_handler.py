from objects import Obstacle, Object
from data_containers import objects as obj_container
from .object_handler import ObjectHandler


class ObstacleHandler(ObjectHandler):
    @classmethod
    def update(cls, obj: Obstacle) -> None:
        if obj.rect.right < obj_container.get_camera().rect.left:
            obj_container.queue_delete(obj)