from enum import IntEnum, auto
import pygame.transform
from pygame import Surface
import core.video
from .object import Rect, Direction, Object


class Velociraptor(Object):
    __slots__ = *Object.__slots__, "direction", "state", 'vel_x', 'vel_y', '_fov'

    class State(IntEnum):
        IDLE = auto(),
        STARTLED = auto(),
        RUNNING = auto(),
        CORNERED = auto(),
        DEAD = auto(),

    ID_STUB: str = "velociraptor_%d"
    SIZE: tuple[float, float] = 8, 7
    TEXTURE_NAME: str = "velociraptor,png"
    TEXTURE_KEY_LEFT: str = f"{TEXTURE_NAME}_{Direction.LEFT}"
    TEXTURE_KEY_RIGHT: str = f"{TEXTURE_NAME}_{Direction.RIGHT}"
    ANIM_INTERVAL: int = 125
    TOTAL_FRAMES: int = 2
    FOV_SIZE: tuple[float, float] = SIZE[0] * 20, SIZE[1] * 5
    VEL_X_MIN: float = 175
    VEL_X_MAX: float = VEL_X_MIN * 2.5
    VEL_X_MAX_IN: float = 1.75  # Seconds to reach maximum speed
    WEIGHT: float = 15.0
    WEIGHT_FACTOR: float = 0.3
    JUMP_ACCEL: float = -(WEIGHT * 8)
    HANDLER_NAME: str = None

    _total: int = 0

    def __init__(self, pos: tuple[int|float, int|float]) -> None:
        Velociraptor._total += 1
        super().__init__(
            id=self.ID_STUB % self._total,
            pos=pos,
            size=self.SIZE
        )

        if not core.video.texture_has(self.TEXTURE_KEY_LEFT):
            flipped_surf: Surface = pygame.transform.flip(
                core.video.texture_get(self.TEXTURE_KEY_RIGHT),
                *Direction.LEFT.value
            )

            flipped_surf.set_colorkey(core.video.COLOR_KEY)

            core.video.texture_add(flipped_surf, self.TEXTURE_KEY_LEFT)

        self.direction: Direction = Direction.LEFT
        self.state = self.State.IDLE
        self.vel_x: float = 0.0
        self.vel_y: float = 0.0
        self.fov: Rect = Rect(*self.rect.center, *self.FOV_SIZE)