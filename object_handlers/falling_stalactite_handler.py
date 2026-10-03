from pygame.time import get_ticks
from objects import Rect, Layer, Direction, Object, Ground, Camera, FallingStalactite
from .object_handler import ObjectHandler


class FallingStalactiteHandler(ObjectHandler):
    @classmethod
    def update(cls, obj: FallingStalactite):
        time_delta = obj.update_delta

        # Your code here ...
        # ...

        obj.last_update = get_ticks()

