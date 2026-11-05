from random import randint
from math import floor
from pygame import Rect as PygameRect
from pygame.time import get_ticks
import core.video
from .object import Object
from .layer import Layer
from .rect import Rect
from .direction import Direction



class HumanBaseForeground(Object):
    __slots__ = (
		*Object.__slots__,
        "option",
        "draw_rect",
    )

    LAYER: Layer = Layer.FOREGROUND_2
    HANDLER_NAME: str = "HumanBaseForegroundHandler"
    ID_STUB: str = "human_base_fg2_%d"
    TEXTURE_NAME: str = "human_base_fg2.png"
    WIDTH: float = 56
    HEIGHT: float = 26
    SIZE: tuple[float, float] = WIDTH, HEIGHT
    Y_POS: float = 168
    MAX_OPTIONS: int = 3
    PARALLAX_FACTOR: float = 1.4
    _total: int = 0

    def __init__(self, pos: tuple[float, float], option: int|None = None) -> None:
        HumanBaseForeground._total += 1
        self.option: int = option if option is not None else randint(0, self.MAX_OPTIONS - 1)
        self.draw_rect: PygameRect = PygameRect(self.WIDTH * self.option, 0, *self.SIZE)

        super().__init__(
            id=self.ID_STUB % self._total,
            pos=pos,
            size=self.SIZE,
            texture_name=self.TEXTURE_NAME
        )

    def draw(self, viewpoint: Rect) -> None:
        viewpoint_parallax: Rect = Rect(
            x=viewpoint.x * self.PARALLAX_FACTOR,
            y=viewpoint.y * self.PARALLAX_FACTOR,
            width=viewpoint.width,
            height=viewpoint.height
        )

        if not viewpoint_parallax.overlaps(self.rect):
            return


        core.video.texture_blit(
            self.texture_name,
            (
                floor(self.x - viewpoint_parallax.x),
                floor(self.y - viewpoint_parallax.y),
            ),
            self.draw_rect
        )