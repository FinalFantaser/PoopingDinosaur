from enum import IntEnum, auto
from math import floor
from random import randint

from pygame import Rect as PygameRect
from pygame.time import get_ticks
import core.video
from .direction import Direction
from .rect import Rect
from .human import Human



class Scientist(Human):
    HANDLER_NAME: str = "ScientistHandler"
    ID_STUB: str = "scientist_%d"
    TEXTURE_NAME: str = "scientist.png"
    DIRECTION_CHANGE_INTERVAL: tuple[int, int] = 1250, 2000
    _total: int = 0

    __slots__ = (
		*Human.__slots__,
        "next_direction_change",
    )

    def __init__(
            self,
            pos: tuple[float, float] = (0, 0),
            state: Human.State = Human.State.IDLE,
            direction: Direction = Direction.LEFT,
    ) -> None:
        Scientist._total += 1

        super().__init__(
            id=self.ID_STUB % self._total,
            texture_name=self.TEXTURE_NAME,
            pos=pos,
            state=state,
            direction=direction,
        )

        self.next_direction_change: int = get_ticks() + randint(*self.DIRECTION_CHANGE_INTERVAL)

    def animate(self) -> None:
        if self.state != self.State.RUNNING:
            return

        curr_ticks = get_ticks()
        if curr_ticks - self.last_frame_change >= self.anim_interval:
            self.curr_frame = (self.curr_frame + 1) % self.total_frames
            self.last_frame_change = curr_ticks

    def draw(self, viewpoint: Rect) -> None:
        if not viewpoint.overlaps(self.rect):
            return

        self.draw_rect.x = int(self.curr_frame * self.width)
        self.draw_rect.y = int((0 if self.state != self.State.RUNNING else 1) * self.height)

        core.video.texture_blit(
            self.texture_name,
            (
                floor(self.x - viewpoint.x),
                floor(self.y - viewpoint.y),
            ),
            self.draw_rect,
        )