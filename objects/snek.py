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
    """
    Attributes:
        SLOWDOWN_TIME: Horizontal complete slowdown time (microseconds).
        TURN_INTERVAL: Interval of direction change in idle state (microseconds).
        last_turn_at: Timestamp of the last direction change in idle state.
    """

    __slots__ = (
		*Dinosaur.__slots__,
        "last_turn_at",
    )

    HANDLER_NAME: str = "SnekHandler"
    ID_STUB: str = 'snek_%d'
    SIZE: tuple[float, float] = 8, 8
    TEXTURE_NAME: str = "snek.png"
    ANIM_INTERVAL: int = 250
    TOTAL_FRAMES: int = 2
    DRAW_AREA: PygameRect = PygameRect(0, 0, *SIZE)
    FOV_SIZE: tuple[float, float] = SIZE[0] * 4, SIZE[1] * 2
    VEL_X_MIN: float = 175
    VEL_X_MAX: float = VEL_X_MIN * 1.5
    VEL_X_MAX_IN: float = 1.75
    WEIGHT: float = 30.0
    SLOWDOWN_TIME: int = 500
    TURN_INTERVAL: int = 500

    _total: int = 0

    def __init__(self, pos: tuple[float, float] = (0, 0)):
        super().__init__(pos)
        self.last_turn_at: int = get_ticks()

    def draw(self, viewpoint: Rect) -> None:
        if not viewpoint.overlaps(self.rect):
            return

        texture_name = f"{self.TEXTURE_NAME}_{self.direction}"

        if self.state == self.State.BITING:
            self.DRAW_AREA.x = 0
            self.DRAW_AREA.y = int(self.SIZE[1])
        elif self.state == self.State.DEAD:
            texture_name = f"{self.TEXTURE_NAME}_{Direction.RIGHT}"
            self.DRAW_AREA.x = 0
            self.DRAW_AREA.y = int(self.SIZE[1]) *2
        else:
            self.DRAW_AREA.x = int(self.curr_frame * self.SIZE[0])
            self.DRAW_AREA.y = 0

        core.video.texture_blit(
            texture_name,
            (
                floor(self.x - viewpoint.x),
                floor(self.y - viewpoint.y),
            ),
            self.DRAW_AREA,
        )

    def animate(self) -> None:
        if self.state == self.State.BITING or self.state == self.State.DEAD:
            return

        last_ticks = get_ticks()
        if last_ticks - self.last_frame_change >= self.ANIM_INTERVAL:
            self.curr_frame = (self.curr_frame + 1) % self.TOTAL_FRAMES
            self.last_frame_change = last_ticks