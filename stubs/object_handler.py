from pygame.time import get_ticks
from objects import Rect, Layer, Direction, Object, Ground, Camera, _HandledObject_
from .object_handler import ObjectHandler
_ParentImports_

class _NewHandlerClass_(_ParentClasses_):
    @classmethod
    def update(cls, obj: _HandledObject_):
        time_delta = obj.update_delta

        # Your code here ...
        # ...

        obj.last_update = get_ticks()

