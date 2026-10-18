from random import randint
from math import floor
from pygame import Rect as PygameRect
from pygame.time import get_ticks
import core.video
from .layer import Layer
from .rect import Rect
from .object import Object
from .direction import Direction
from .dinosaur import Dinosaur


class Zephyrosaurus(Dinosaur):
    """
    BURROW_TIME_RANGE: range of time (ms) after startling when the dinosaur burrows.
    BURROW_TIME: How fast the dinosaur burrows (ms).
    BURROW_PER_MS: Fraction of per-pixel progress within one ms (cached to avoid calculating each time).
    startled_at: Timestamp (python.time.get_ticks) when the dinosaur got startled. `0` immediately after spawn.
    burrow_time: Time before the dinosaur burrows. Initialized after startling: `startled_at` + `randint(BURROW_TIME_RANGE)`.
    burrow_progress: How deep is the dinosaur currently burrowed.
    """

    __slots__ = (
		*Dinosaur.__slots__,
        "startled_at",
        "burrow_time",
        "burrow_progress",
        # Your slots here ...
    )

    HANDLER_NAME: str = "ZephyrosaurusHandler"
    ID_STUB: str = "zephyrosaurus_%d"
    WIDTH: float = 18
    HEIGHT: float = 9
    SIZE: tuple[float, float] = WIDTH, HEIGHT
    TEXTURE_NAME: str = "zephyrosaurus.png"
    ANIM_INTERVAL: int = 250
    TOTAL_FRAMES: int = 2
    DRAW_AREA: PygameRect = PygameRect(0, 0, *SIZE)
    FOV_SIZE: tuple[float, float] = core.video.get_screen_rect().width / 2, core.video.get_screen_rect().height / 4
    VEL_X_MIN: float = 175
    VEL_X_MAX: float = VEL_X_MIN * 2
    VEL_X_MAX_IN: float = 1.75  # Seconds to reach maximum speed
    INVINCIBILITY_DURATION = 1000
    WEIGHT: float = 35.0
    WEIGHT_FACTOR: float = 0.6
    JUMP_ACCEL: float = -(WEIGHT * 4)
    BURROW_TIME_RANGE: tuple[int, int] = 1000, 2000
    BURROW_TIME: int = 500
    BURROW_PER_MS: float = HEIGHT / BURROW_TIME

    _total: int = 0

    def __init__(self, pos: tuple[float, float] = (0, 0)):
        super().__init__(pos)
        self.direction = Direction.LEFT
        self.startled_at: int = 0
        self.burrow_time: int = 0
        self.burrow_progress: float = 0

    def draw(self, viewpoint: Rect) -> None:
        # For this class, the CORNERED state is used for burrowing
        if self.state != self.State.CORNERED:
            super().draw(viewpoint)
            return

        y_diff = self.burrow_progress * self.BURROW_PER_MS

        draw_area = Rect.from_pygame_rect(self.DRAW_AREA)
        draw_area.x = self.curr_frame * self.WIDTH
        draw_area.height -= y_diff

        core.video.texture_blit(
            f"{self.TEXTURE_NAME}_{self.direction}",
            (
                floor(self.x - viewpoint.x),
                floor(self.y + y_diff - viewpoint.y),
            ),
            draw_area.to_pygame_rect(),
        )