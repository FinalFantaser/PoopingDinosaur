from math import floor
from pygame import Rect as PygameRect
from pygame.time import get_ticks
import core.video
from .object import Object
from .layer import Layer
from .direction import Direction
from .dinosaur import Dinosaur


class Zephyrosaurus(Dinosaur):
    __slots__ = (
		*Dinosaur.__slots__,
        "startled_at",
        "burrow_time",
        # Your slots here ...
    )

    HANDLER_NAME: str = "ZephyrosaurusHandler"
    ID_STUB: str = "zephyrosaurus_%d"

    _total: int = 0