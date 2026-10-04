from math import floor
from pygame import Rect as PygameRect
from pygame.time import get_ticks
import core.video
from . import Rect
from .object import Object
from .layer import Layer
from .direction import Direction
from .dinosaur import Dinosaur


class Snek(Dinosaur):
    __slots__ = (
		*Dinosaur.__slots__,
        # Your slots here ...
    )

    HANDLER_NAME: str = "SnekHandler"
    ID_STUB: str = 'snek_%d'
    SIZE: tuple[float, float] = 8, 8
    TEXTURE_NAME: str = "snek.png"
    FOV_SIZE: tuple[float, float] = SIZE[0] * 4, SIZE[1] * 2
    VEL_X_MIN: float = 175
    VEL_X_MAX: float = VEL_X_MIN * 1.5
    VEL_X_MAX_IN: float = 1.75
    WEIGHT: float = 30.0

    _total: int = 0

    def animate(self) -> None:
        if self.state == self.State.BITING:
            return

        super().animate()