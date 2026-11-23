from enum import IntEnum, auto
from pygame import Rect as PygameRect
import core.video
from .direction import Direction
from .rect import Rect
from .object_with_physics import ObjectWithPhysics


class Human(ObjectWithPhysics):
    class State(IntEnum):
        IDLE = auto()
        STARTLED = auto()
        RUNNING = auto()
        SHOOTING = auto()

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

    __slots__ = (
		*ObjectWithPhysics.__slots__,
        "invincibility",
        "health",
        "state",
        "direction",
        "_fov",
        "draw_rect",
    )

    def __init__(
            self,
            id: str,
            texture_name: str,
            pos: tuple[float, float] = (0, 0),
            state: State = State.IDLE,
            direction: Direction = Direction.LEFT,
    ) -> None:
        super().__init__(
            id=id,
            pos=pos,
            size=self.SIZE,
            texture_name=texture_name,
            total_frames=self.TOTAL_FRAMES,
            anim_interval=self.ANIM_INTERVAL,
        )

        self.invincibility: int = 0
        self.health = 1
        self.state: Human.State = state
        self.direction: Direction = direction
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

    def die(self) -> None:
        # Humans are more resistant to tyrannosaurus poo :)
        pass