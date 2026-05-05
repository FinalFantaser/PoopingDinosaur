from objects import Poo, Ground
from object_handlers.object_handler import ObjectHandler
from data_containers import objects as obj_container


class PooHandler(ObjectHandler):
    @classmethod
    def update(cls, obj: Poo) -> None:
        if not obj_container.get_camera().within_viewpoint(obj):
            obj_container.queue_delete(obj)
            return

        ground: Ground = obj_container.get_ground()

        # Gravity
        if obj.rect.bottom < ground.touch_level:
            obj.vel_y += obj.vel_y / 2
        else:
            obj.vel_y = 0

        accel_y: float = obj.vel_y / 1000 * obj.update_delta
        obj.y = min(obj.y + accel_y, ground.touch_level)

