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

    ID_STUB: str = "zombiesaurus_%d"
    HANDLER_NAME: str = "ZombiesaurusHandler"
    SIZE: tuple[float, float] = 40, 14
    SIZE_BODY: tuple[float, float] = 31, 14
    SIZE_HEAD: tuple[float, float] = 10, 11
    HEAD_POS: tuple[float, float] = -1, 0
    TEXTURE_NAME: str = "zombiesaurus.png"
    ANIM_INTERVAL_HEAD: int = 100
    TOTAL_FRAMES_HEAD: int = 3
    DRAW_AREA: PygameRect = PygameRect(0, 0, *SIZE_BODY)
    DRAW_AREA_HEAD: PygameRect = PygameRect(0, 28, *SIZE_HEAD)
    HITBOX_BITE_SIZE: tuple[float, float] = SIZE_HEAD
