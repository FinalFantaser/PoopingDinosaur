from typing import Self
from random import randint
from math import floor
from pygame import Rect as PygameRect
from pygame.time import get_ticks
import core.video
from .rect import Rect
from .object import Object


class Tesla(Object):
    __slots__ = (
        *Object.__slots__,
        "charge",
        "charge_interval",
        "left",
        "right",
        "gap",
        "draw_rect",
    )

    HANDLER_NAME: str = "TeslaHandler"
    TEXTURE_NAME: str = "tesla.png"
    ID_STUB: str = "tesla_%d"
    WIDTH: int = 14
    HEIGHT: int = 16
    SIZE: tuple[float, float] = WIDTH, HEIGHT
    TOTAL_FRAMES: int = 2
    ANIM_INTERVAL: int = 250
    CHARGE_MAX: float = 1000
    CHARGE_INTERVALS: tuple[float, ...] = 1500, 2000
    GAP_RANGE: tuple[int, int] = 4, 8

    _total: int = 0

    def __init__(self, pos: tuple[float, float]) -> None:
        Tesla._total += 1

        super().__init__(
            id=self.ID_STUB % self._total,
            pos=pos,
            size=self.SIZE,
            texture_name=self.TEXTURE_NAME,
            total_frames=self.TOTAL_FRAMES,
            anim_interval=self.ANIM_INTERVAL,
        )

        self.charge: float = 0.0
        self.charge_interval: float = randint(*self.CHARGE_INTERVALS)
        self.left: str|None = None
        self.right: str|None = None
        self.gap: int = randint(*self.GAP_RANGE)
        self.draw_rect: PygameRect = PygameRect(0, 0, *self.size)

    def connect(self, other_tesla: Self) -> Self:
        """
        Connect to another tesla. Sets `left` and `right` to each other respectively.
        Charge level and interval are set as for the `left` tesla.

        **self is left, and other_tesla is right:**

        **self** <-------> **other_tesla**
        """
        self.right = other_tesla.id
        other_tesla.left = self.id
        other_tesla.charge_interval = self.charge_interval
        other_tesla.charge = self.charge

        return self

    def animate(self) -> None:
        curr_ticks = get_ticks()

        if curr_ticks - self.last_frame_change < self.anim_interval:
            return

        if self.charge > self.CHARGE_MAX * 0.75:
            self.curr_frame = (self.curr_frame + 1) % self.total_frames

    def draw(self, viewpoint: Rect) -> None:
        if not viewpoint.overlaps(self.rect):
            return

        self.draw_rect.x = int(self.curr_frame * self.width)

        core.video.texture_blit(
            self.texture_name,
            (
                floor(self.x - viewpoint.x),
                floor(self.y - viewpoint.y),
            ),
            self.draw_rect
        )