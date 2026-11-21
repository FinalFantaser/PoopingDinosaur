from enum import IntEnum, auto
from math import floor

from pygame import Rect as PygameRect
from pygame.time import get_ticks
import core.video
from .direction import Direction
from .rect import Rect
from .object_with_physics import ObjectWithPhysics



class Scientist(ObjectWithPhysics):
    class State(IntEnum):
        IDLE = auto()
        STARTLED = auto()
        RUNNING = auto()

    HANDLER_NAME: str = "ScientistHandler"
    ID_STUB: str = "scientist_%d"
    TEXTURE_NAME: str = "scientist.png"
    WIDTH: float = 8
    HEIGHT: float = 8
    SIZE: tuple[float, float] = WIDTH, HEIGHT
    TOTAL_FRAMES: int = 2
    ANIM_INTERVAL: int = 250
    JUMP_ACCEL: int = 100
    WEIGHT: float = 75
    WEIGHT_FACTOR: float = 0.5
    HEALTH_MAX: int = 1
    INVINCIBILITY_DURATION: int = 0
    _total: int = 0

    __slots__ = (
		*ObjectWithPhysics.__slots__,
        "invincibility",
        "health",
        "state",
        "direction",
        "last_direction_change",
        "draw_rect",
    )

    def __init__(
            self,
            pos: tuple[float, float] = (0, 0),
            state: State = State.IDLE,
            direction: Direction = Direction.LEFT,
    ) -> None:
        Scientist._total += 1

        super().__init__(
            id=self.ID_STUB % self._total,
            pos=pos,
            size=self.SIZE,
            texture_name=self.TEXTURE_NAME,
            total_frames=self.TOTAL_FRAMES,
            anim_interval=self.ANIM_INTERVAL,
        )

        self.invincibility: int = 0
        self.health = 1
        self.state: Scientist.State = state
        self.direction: Direction = direction
        self.last_direction_change: int = get_ticks()
        self.draw_rect: PygameRect = PygameRect(0, 0, *self.size)

    @property
    def hitbox(self) -> Rect:
        return self.rect

    @property
    def weight(self) -> float:
        return self.WEIGHT

    def animate(self) -> None:
        if self.state == self.State.IDLE:
            return

        curr_ticks = get_ticks()
        if curr_ticks - self.last_frame_change >= self.anim_interval:
            self.curr_frame = (self.curr_frame + 1) % self.total_frames
            self.last_frame_change = curr_ticks

    def draw(self, viewpoint: Rect) -> None:
        self.draw_rect.x = int(self.curr_frame * self.width)
        self.draw_rect.y = int((0 if self.state == self.State.RUNNING else 1) * self.height)

        core.video.texture_blit(
            self.texture_name,
            (
                floor(self.x - viewpoint.x),
                floor(self.y - viewpoint.y),
            ),
            self.draw_rect,
        )