from random import randint
from math import floor
from pygame import Rect as PygameRect
from pygame.time import get_ticks
import core.video
from . import Rect
from .object import Object
from .layer import Layer
from .direction import Direction



class HumanBaseBackground(Object):
    __slots__ = (
		*Object.__slots__,
        "option",
        "draw_rect",
    )

    HANDLER_NAME: str = "HumanBaseBackgroundHandler"
    ID_STUB: str = "human_base_bg2_%d"
    TEXTURE_NAME: str = "human_base_bg2.png"
    WIDTH: float = 32
    HEIGHT: float = 40
    SIZE: tuple[float, float] = WIDTH, HEIGHT
    Y_POS: float = 102
    MAX_OPTIONS: int = 3
    _total: int = 0

    def __init__(self, pos: tuple[float, float], option: int|None = None) -> None:
        HumanBaseBackground._total += 1
        self.option: int = option if option is not None else randint(0, self.MAX_OPTIONS - 1)
        self.draw_rect: PygameRect = PygameRect(self.WIDTH * self.option, 0, *self.SIZE)

        super().__init__(
            id=self.ID_STUB % self._total,
            pos=pos,
            size=self.SIZE,
            texture_name=self.TEXTURE_NAME
        )

    def draw(self, viewpoint: Rect) -> None:
        core.video.texture_blit(
            self.texture_name,
            (
                floor(self.x - viewpoint.x),
                floor(self.y - viewpoint.y),
            ),
            self.draw_rect
        )