from pygame.time import get_ticks
from objects import Rect, Layer, Direction, Object, Ground, Camera, Snek
from .object_handler import ObjectHandler
from data_containers import objects as obj_container, game_data


class SnekHandler(ObjectHandler):
    @classmethod
    def update(cls, obj: Snek):
        time_delta = obj.update_delta

        # Your code here ...
        # ...

        obj.last_update = get_ticks()

