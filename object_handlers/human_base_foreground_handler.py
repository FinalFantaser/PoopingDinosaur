from pygame.time import get_ticks
from objects import Rect, Layer, Direction, Object, Ground, Camera, HumanBaseForeground
from .object_handler import ObjectHandler
from data_containers import objects as obj_container, game_data


class HumanBaseForegroundHandler(ObjectHandler):
    @classmethod
    def update(cls, obj: HumanBaseForeground):
        if cls.delete_if_passed_camera(obj):
            return

        obj.last_update = get_ticks()

    @classmethod
    def delete_if_passed_camera(cls, obj: HumanBaseForeground):
        parallax_camera = obj_container.get_camera().rect.with_parallax(HumanBaseForeground.PARALLAX_FACTOR)

        if obj.rect.right < parallax_camera.x:
            obj_container.queue_delete(obj)

