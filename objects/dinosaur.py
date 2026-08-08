import core
import pygame.transform, pygame.time
from pygame import Surface, Rect as PygameRect
from enum import IntEnum, auto
from .direction import Direction
from .rect import Rect
from .object import Object

class Dinosaur(Object):
    """
    Basic dinosaur class with common features. The properties are limited since dinosaurs mostly run all the time.

    Attributes:
        ID_STUB: Stub for an object id. Typically, it's a dinosaur's name with total count.
        SIZE: Size of the dinosaur.
        TEXTURE_NAME: Name of a texture used.
        ANIM_INTERVAL: Basic interval of animation frame change.
        TOTAL_FRAMES: Total number of frames.
    """

    __slots__ = *Object.__slots__, "direction", "state", 'vel_x', 'vel_y', '_fov'

    class State(IntEnum):
        """
        Finite states determining dinosaur's behavior.

        Attributes:
            IDLE: Dinosaur is idle, chilling.
            STARTLED: Dinosaur sees an enemy for the first time.
            RUNNING: Dinosaur runs away from its enemies.
            CHASING: Dinosaur chases its prey.
            CORNERED: Dinosaur got nowhere to run and panics, waiting to get eaten.
            BITING: Dinosaur tries to bite its prey.
            DEAD: Dinosaur is dead.
        """
        IDLE = auto(),
        STARTLED = auto(),
        RUNNING = auto(),
        CHASING = auto(),
        CORNERED = auto(),
        BITING = auto(),
        DEAD = auto(),

    ID_STUB: str = "dinosaur_%d"
    SIZE: tuple[float, float] = 0, 0
    TEXTURE_NAME: str = "dinosaur.png"
    ANIM_INTERVAL: int = 250
    TOTAL_FRAMES: int = 2
    DRAW_AREA: PygameRect = PygameRect(0, 0, *SIZE)
    FOV_SIZE: tuple[float, float] = core.video.get_screen_rect().width / 2, core.video.get_screen_rect().height / 4
    VEL_X_MIN: float = 175
    VEL_X_MAX: float = VEL_X_MIN * 2.5
    VEL_X_MAX_IN: float = 1.75  # Seconds to reach maximum speed
    WEIGHT: float = 15.0
    WEIGHT_FACTOR: float = 0.3
    JUMP_ACCEL: float = -(WEIGHT * 8)

    _total: int = 0

    def __init__(self, pos: tuple[int|float, int|float]) -> None:
        self.__class__._total += 1
        super().__init__(
            id=self.ID_STUB % self._total,
            pos=pos,
            size=self.SIZE
        )

        core.video.texture_load(core.paths.TEXTURES / self.TEXTURE_NAME, f"{self.TEXTURE_NAME}_{Direction.RIGHT}")

        if not core.video.texture_has(f"{self.TEXTURE_NAME}_{Direction.LEFT}"):
            flipped_surf: Surface = pygame.transform.flip(
                core.video.texture_get(f"{self.TEXTURE_NAME}_{Direction.RIGHT}"),
                *Direction.LEFT.value
            )

            flipped_surf.set_colorkey(core.video.COLOR_KEY)

            core.video.texture_add(flipped_surf, f"{self.TEXTURE_NAME}_{Direction.LEFT}")

        self.direction: Direction = Direction.LEFT
        self.state = self.State.IDLE
        self.vel_x: float = 0.0
        self.vel_y: float = 0.0
        self._fov: Rect = Rect(*self.rect.center, *self.FOV_SIZE)

    @property
    def fov_around(self) -> Rect:
        self._fov.center = self.rect.center
        return self._fov

    @property
    def fov_ahead(self) -> Rect:
        return Rect(
            self.rect.left - self.fov_around.width / 2 if self.direction == Direction.LEFT else self.rect.right,
            self.rect.y,
            self.fov_around.width / 2,
            self.fov_around.height
        )

    @property
    def hitbox(self) -> Rect:
        return self.rect

    def draw(self, viewpoint: Rect) -> None:
        if not viewpoint.overlaps(self.rect):
            return

        texture_name: str

        if self.state == self.State.DEAD:
            texture_name = f"{self.TEXTURE_NAME}_{Direction.RIGHT}"
            self.DRAW_AREA.x = 0
            self.DRAW_AREA.y = int(self.SIZE[1])
        else:
            texture_name = f"{self.TEXTURE_NAME}_{self.direction}"
            self.DRAW_AREA.x = int(self.curr_frame * self.SIZE[0])
            self.DRAW_AREA.y = 0

        core.video.texture_blit(
            texture_name,
            (self.x - viewpoint.x, self.y - viewpoint.y),
            self.DRAW_AREA,
        )

    def animate(self) -> None:
        if self.vel_x == 0.0 or self.state == self.State.DEAD:
            return

        # Run animation interval is affected by dinosaur's current speed
        anim_interval: int = int(self.ANIM_INTERVAL * min(self.VEL_X_MAX / self.vel_x, 2))

        if pygame.time.get_ticks() - self.last_frame_change >= anim_interval:
            self.curr_frame = (self.curr_frame + 1) % self.TOTAL_FRAMES
            self.last_frame_change = pygame.time.get_ticks()