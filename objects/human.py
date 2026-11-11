from math import floor
from pygame import Rect as PygameRect
from pygame.time import get_ticks
import core.video
from .direction import Direction
from .rect import Rect
from .layer import Layer
from .object import Object



class Human(Object):
    """Basic class for human NPCs"""

    __slots__ = (
		*Object.__slots__,
        # Your slots here ...
    )

    