from pygame.time import get_ticks
from objects import Rect, Layer, Direction, Object, Ground, Camera, Skyscraper
from .object_handler import ObjectHandler
from data_containers import objects as obj_container, game_data


class SkyscraperHandler(ObjectHandler):
    @classmethod
    def update(cls, obj: Skyscraper):
        time_delta = obj.update_delta

        # Your code here ...
        # ...

        obj.last_update = get_ticks()

