from pygame.time import get_ticks
from objects import Rect, Layer, Direction, Object, Ground, Camera, Zephyrosaurus
from .object_handler import ObjectHandler
from data_containers import objects as obj_container, game_data
from .dinosaur_handler import DinosaurHandler

class ZephyrosaurusHandler(DinosaurHandler):
    @classmethod
    def update(cls, obj: Zephyrosaurus):
        time_delta = obj.update_delta

        # Your code here ...
        # ...

        obj.last_update = get_ticks()

