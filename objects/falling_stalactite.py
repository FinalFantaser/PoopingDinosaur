from math import floor
from random import choice
from pygame.time import get_ticks
import core.video
import core.gui
from .rect import Rect
from .object import Object

class FallingStalactite(Object):
    __slots__ = (
		*Object.__slots__,
        "dead",
        "drop_exists",
        "drop_pos",
        "last_dropped_at",
    )

    HANDLER_NAME: str = "FallingStalactiteHandler"
    ID_STUB: str = "stalactite_%d"
    TEXTURE_NAME: str = "stalactite.png"
    WIDTH: float = 13
    HEIGHT: float = 16
    SIZE: tuple[float, float] = WIDTH, HEIGHT

    DROP_COLOR: str = core.gui.COLOR_BG
    DROP_SPEED: float = 300
    DROP_INTERVAL: int = 250

    _total: int = 0

    def __init__(self, pos: tuple[float, float] = (0, 0), dead: bool|None = None) -> None:
        FallingStalactite._total += 1

        super().__init__(
            id=self.ID_STUB % self._total,
            pos=pos,
            size=self.SIZE,
            texture_name=self.TEXTURE_NAME
        )

        self.dead: bool = dead if dead is not None else choice([True, False])
        self.drop_exists: bool = False
        self.drop_pos: tuple[float, float] = pos
        self.last_dropped_at: float = self.last_update

    def draw(self, viewpoint: Rect) -> None:
        if not viewpoint.overlaps(self.rect):
            return

        draw_x = floor(self.x - viewpoint.x)
        draw_y = floor(self.y - viewpoint.y)

        core.video.texture_blit(
            self.texture_name,
            (draw_x, draw_y),
        )

        # If not dead, if there is a drop, draw the drap
        if not self.dead and self.drop_exists:
            core.video.draw_pixel(
                (
                    floor(self.drop_pos[0] - viewpoint.x),
                    floor(self.drop_pos[1] - viewpoint.y),
                ),
                self.DROP_COLOR,
            )