from pygame.time import get_ticks
from objects import Rect, Layer, Direction, Object, Ground, Camera, HumanBaseBackground
from .object_handler import ObjectHandler
from data_containers import objects as obj_container, game_data


class HumanBaseBackgroundHandler(ObjectHandler):
    @classmethod
    def update(cls, obj: HumanBaseBackground):
        if cls.delete_if_passed_camera(obj):
            return

        obj.last_update = get_ticks()

