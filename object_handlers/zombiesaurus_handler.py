from pygame.time import get_ticks
from objects import Rect, Layer, Direction, Object, Ground, Camera, Zombiesaurus
from .object_handler import ObjectHandler
from data_containers import objects as obj_container, game_data
from .dinosaur_handler import DinosaurHandler

class ZombiesaurusHandler(DinosaurHandler):
    @classmethod
    def update(cls, obj: Zombiesaurus):
        time_delta = obj.update_delta

        # Your code here ...
        # ...

        obj.last_update = get_ticks()

