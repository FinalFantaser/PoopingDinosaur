from math import floor
from pygame import Rect as PygameRect
from pygame.time import get_ticks
import core.video
from .object import Object
from .layer import Layer
from .direction import Direction
from .separate_head_dinosaur import SeparateHeadDinosaur


class Zombiesaurus(SeparateHeadDinosaur):
    __slots__ = (
		*SeparateHeadDinosaur.__slots__,
        # Your slots here ...
    )

    HANDLER_NAME: str = "ZombiesaurusHandler"