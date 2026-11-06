from pygame.time import get_ticks
from objects import Rect, Layer, Direction, Object, Ground, Camera, LandMine
from .object_handler import ObjectHandler
from data_containers import objects as obj_container, game_data


class LandMineHandler(ObjectHandler):
    @classmethod
    def update(cls, obj: LandMine):
        time_delta = obj.update_delta

        # Your code here ...
        # ...

        obj.last_update = get_ticks()

