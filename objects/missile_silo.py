from enum import IntEnum
from math import floor
from pygame import Rect as PygameRect
from pygame.time import get_ticks
import core.video
from .direction import Direction
from .rect import Rect
from .layer import Layer
from .object import Object



class MissileSilo(Object):
    __slots__ = (
		*Object.__slots__,
        "state",
        "button_hitbox",
        "draw_area",
    )

    class State(IntEnum):
        READY = 0,
        LAUNCHING = 1,
        EMPTY = 1,

    HANDLER_NAME: str = "MissileSiloHandler"
    ID_STUB: str = "missile_silo_%d"
    TEXTURE_NAME: str = "missile_silo.png"
    WIDTH: float = 32
    HEIGHT: float = 8
    SIZE: tuple[float, float] = WIDTH, HEIGHT
    TOTAL_FRAMES: int = 2
    ANIM_INTERVAL: int = 250
    BUTTON_HITBOX_TEMPLATE: Rect = Rect(24, 0, 8, 6)

    _total: int = 0

    def __init__(self, pos: tuple[float, float] = (0, 0)) -> None:
        MissileSilo._total += 1

        super().__init__(
            id=self.ID_STUB % self._total,
            pos=pos,
            size=self.SIZE,
            texture_name=self.TEXTURE_NAME,
            total_frames=self.TOTAL_FRAMES,
            anim_interval=self.ANIM_INTERVAL,
        )

        self.state: MissileSilo.State = self.State.READY
        self.button_hitbox: Rect = Rect(
            self.x + self.BUTTON_HITBOX_TEMPLATE.x,
            self.y + self.BUTTON_HITBOX_TEMPLATE.y,
            *self.BUTTON_HITBOX_TEMPLATE.size,
        )

        self.draw_area: PygameRect = PygameRect(0, 0, *self.SIZE)

    def animate(self) -> None:
        if self.state != self.State.READY:
            return

        curr_ticks = get_ticks()
        if curr_ticks - self.last_frame_change >= self.anim_interval:
            self.last_frame_change = curr_ticks
            self.curr_frame = (self.curr_frame + 1) % self.total_frames

    def draw(self, viewpoint: Rect) -> None:
        if not viewpoint.overlaps(self.rect):
            return

        self.draw_area.x = self.curr_frame * self.width
        self.draw_area.y = self.state.value * self.height
        
        core.video.texture_blit(
            self.texture_name,
            (
                floor(self.x - viewpoint.x),
                floor(self.y - viewpoint.y),
            ),
            self.draw_area
        )