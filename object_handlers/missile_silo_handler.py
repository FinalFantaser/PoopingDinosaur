from pygame.time import get_ticks
from objects import Rect, Layer, Direction, Object, Ground, Camera, MissileSilo
from .object_handler import ObjectHandler
from data_containers import objects as obj_container, game_data


class MissileSiloHandler(ObjectHandler):
    @classmethod
    def update(cls, obj: MissileSilo):
        if cls.delete_if_passed_camera(obj):
            return

        obj.button_hitbox.y = obj.y

        time_delta = obj.update_delta

        obj.last_update = get_ticks()

