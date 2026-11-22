from enum import IntEnum, auto
from math import floor
from random import randint

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
    VEL_X: float = 90
    JUMP_ACCEL: float = -100
    WEIGHT: float = 75
    WEIGHT_FACTOR: float = 1
    HEALTH_MAX: int = 1
    INVINCIBILITY_DURATION: int = 0
    FOV_SIZE: tuple[float, float] = core.video.get_screen_rect().width / 3, HEIGHT * 4
    DIRECTION_CHANGE_INTERVAL: tuple[int, int] = 1250, 2000
    _total: int = 0

    __slots__ = (
		*ObjectWithPhysics.__slots__,
        "invincibility",
        "health",
        "state",
        "direction",
        "next_direction_change",
        "_fov",
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
        self.next_direction_change: int = get_ticks() + randint(*self.DIRECTION_CHANGE_INTERVAL)
        self._fov: Rect = Rect(*self.pos, *self.FOV_SIZE)
        self.draw_rect: PygameRect = PygameRect(0, 0, *self.size)

    @property
    def hitbox(self) -> Rect:
        return self.rect

    @property
    def fov(self) -> Rect:
        self._fov.center_x = self.rect.center_x
        self._fov.bottom = self.rect.bottom

        return self._fov

    @property
    def weight(self) -> float:
        return self.WEIGHT

    def animate(self) -> None:
        if self.state != self.State.RUNNING:
            return

        curr_ticks = get_ticks()
        if curr_ticks - self.last_frame_change >= self.anim_interval:
            self.curr_frame = (self.curr_frame + 1) % self.total_frames
            self.last_frame_change = curr_ticks

    def draw(self, viewpoint: Rect) -> None:
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