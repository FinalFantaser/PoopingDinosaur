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
    SIZE: tuple[float, float] = 18, 9
    TEXTURE_NAME: str = "zephyrosaurus.png"
    ANIM_INTERVAL: int = 250
    TOTAL_FRAMES: int = 2
    DRAW_AREA: PygameRect = PygameRect(0, 0, *SIZE)
    FOV_SIZE: tuple[float, float] = core.video.get_screen_rect().width / 2, core.video.get_screen_rect().height / 4
    VEL_X_MIN: float = 175
    VEL_X_MAX: float = VEL_X_MIN * 2.5
    VEL_X_MAX_IN: float = 1.75  # Seconds to reach maximum speed
    INVINCIBILITY_DURATION = 1000
    WEIGHT: float = 35.0
    WEIGHT_FACTOR: float = 0.6
    JUMP_ACCEL: float = -(WEIGHT * 8)

    _total: int = 0