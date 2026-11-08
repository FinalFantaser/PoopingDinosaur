from typing import Self
from math import floor
from pygame import Rect as PygameRect
from pygame.time import get_ticks
import core.video
from .rect import Rect
from .object import Object


class LandMine(Object):
    __slots__ = (
        *Object.__slots__,
        "trigger_area",
        "triggered_at",
    )

    HANDLER_NAME: str = "LandMineHandler"
    TEXTURE_NAME: str = "land_mine.png"
    ID_STUB: str = "land_mine_%d"
    WIDTH: int = 16
    HEIGHT: int = 6
    SIZE: tuple[float, float] = WIDTH, HEIGHT
    TOTAL_FRAMES: int = 2
    ANIM_INTERVAL: int = 500
    DRAW_AREA: PygameRect = PygameRect(0, 0, *SIZE)
    TRIGGER_AREA_WIDTH: float = 96
    TRIGGER_AREA_HEIGHT: float = 32
    TRIGGER_AREA_SIZE: tuple[float, float] = TRIGGER_AREA_WIDTH, TRIGGER_AREA_HEIGHT
    TRIGGER_DELAY: int = 1000  # In ms
 
    _total: int = 0

    def __init__(self, pos: tuple[float, float] = (0, 0)) -> None:
        LandMine._total += 1

        super().__init__(
            id=self.ID_STUB % self._total,
            pos=pos,
            size=self.SIZE,
            texture_name=self.TEXTURE_NAME,
            total_frames=self.TOTAL_FRAMES,
            anim_interval=self.ANIM_INTERVAL,
        )

        self.trigger_area: Rect = Rect(*self.pos, *self.TRIGGER_AREA_SIZE)
        self.trigger_area.center_x = self.rect.center_x

        self.triggered_at: None|int = None

    def draw(self, viewpoint: Rect) -> None:
        self.DRAW_AREA.x = self.curr_frame * self.width

        core.video.texture_blit(
            self.texture,
            (
                floor(self.x - viewpoint.x),
                floor(self.y - viewpoint.y),
            ),
            self.DRAW_AREA
        )

    def animate(self) -> None:
        curr_ticks = get_ticks()
        if curr_ticks - self.last_frame_change >= self.anim_interval:
            self.curr_frame = (self.curr_frame + 1) % self.TOTAL_FRAMES
            self.last_frame_change = curr_ticks

    def put_on_ground(self, touch_level: float) -> Self:
        self.rect.bottom = touch_level
        self.trigger_area.y = self.y
        return self
