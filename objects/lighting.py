from random import choice
from math import floor
from pygame import Rect as PygameRect
from pygame.time import get_ticks
import core.video
from .rect import Rect
from .object import Object


class Lighting(Object):
    __slots__ = (
		*Object.__slots__,
        "started_at",
        "draw_rect",
    )

    HANDLER_NAME: str = "LightingHandler"
    TEXTURE_NAME: str = "lighting.png"
    ID_STUB: str = "lighting_%d"
    WIDTH: float = 16
    HEIGHT: float = 32
    SIZE: tuple[float, float] = WIDTH, HEIGHT
    TOTAL_FRAMES: int = 2
    ANIM_INTERVAL: int = 100
    FRAME_RAND_RANGE: tuple[int, int] = -100, 100
    LIFESPAN: int = 750  # In ms

    _total: int = 0

    def __init__(self, pos: tuple[float, float] = (0, 0)) -> None:
        Lighting._total += 1

        super().__init__(
            id=self.ID_STUB % self._total,
            pos=pos,
            size=self.SIZE,
            texture_name=self.TEXTURE_NAME,
            total_frames=self.TOTAL_FRAMES,
            anim_interval=self.ANIM_INTERVAL
        )

        self.last_frame_change += choice(self.FRAME_RAND_RANGE)
        self.started_at: int = get_ticks()
        self.draw_rect: PygameRect = PygameRect(0, 0, *self.size)

    def animate(self) -> None:
        curr_ticks = get_ticks()
        if curr_ticks - self.last_frame_change >= self.anim_interval:
            self.curr_frame = (self.curr_frame + 1) % self.total_frames
            self.last_frame_change = curr_ticks

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
            self.draw_rect,
        )