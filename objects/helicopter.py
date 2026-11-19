from math import floor
from random import randint
from pygame import Rect as PygameRect
from pygame.time import get_ticks
import core.video
from .direction import Direction
from .rect import Rect
from .object import Object
from .object_with_physics import ObjectWithPhysics


class Helicopter(ObjectWithPhysics):
    __slots__ = (
        *ObjectWithPhysics.__slots__,
        "draw_rect",
        "bombs",
        "engine_power_x",
        "engine_power_y",
        "last_bomb_at",
        "next_bomb_at",
    )

    HANDLER_NAME: str = "HelicopterHandler"
    ID_STUB: str = "helicopter_%d"
    TEXTURE_NAME: str = "helicopter.png"
    WIDTH: float = 16
    HEIGHT: float = 16
    SIZE: tuple[float, float] = WIDTH, HEIGHT
    TOTAL_FRAMES: int = 2
    ANIM_INTERVAL: int = 150

    ALTITUDE_MAX: float = HEIGHT * 2
    ALTITUDE_MIN: float = HEIGHT * 4
    TARGET_TRACKING_MIN = -WIDTH * 3
    TARGET_TRACKING_MAX = WIDTH * 3
    VEL_X_MIN: float = 175
    VEL_Y_CONST: float = 100
    ENGINE_POWER_X_MIN: float = -1
    ENGINE_POWER_X_MAX: float = 2
    ENGINE_POWER_Y_MIN: float = -1
    ENGINE_POWER_Y_MAX: float = 1
    ENGINE_POWER_X: float = (ENGINE_POWER_X_MAX - ENGINE_POWER_X_MIN) / 1000  # Per ms
    ENGINE_POWER_Y: float = (ENGINE_POWER_Y_MAX - ENGINE_POWER_Y_MIN) / 750  # Per ms
    WEIGHT_FACTOR: float = 0.3
    BOMBS_MAX: int = 3
    BOMBS_INTERVAL_RANGE: tuple[int, int] = 1500, 2500  # In ms
    BOMBS_INDICATOR_POS: tuple[int, int] = 8, 11
    BOMBS_INDICATOR_COLOR: str = "0xFFFFFF"
    BOMBS_DELAY_AFTER_SPAWN: int = 2000  # In ms
    DELAY_BEFORE_RETREAT: int = 1000  # In ms

    _total: int = 0

    def __init__(self, pos: tuple[float, float] = (0, 0)) -> None:
        Helicopter._total += 1

        super().__init__(
            id=self.ID_STUB % self._total,
            pos=pos,
            size=self.SIZE,
            texture_name=self.TEXTURE_NAME,
            total_frames=self.TOTAL_FRAMES,
            anim_interval=self.ANIM_INTERVAL,
        )

        self.draw_rect: PygameRect = PygameRect(0, 0, *self.SIZE)
        self.bombs: int = self.BOMBS_MAX
        self.engine_power_x: float = 0
        self.engine_power_y: float = 0
        self.last_bomb_at: int = get_ticks() + self.BOMBS_DELAY_AFTER_SPAWN
        self.next_bomb_at: int = self.calculate_next_bomb()

    def calculate_next_bomb(self) -> int:
        return self.last_bomb_at + randint(*self.BOMBS_INTERVAL_RANGE)

    def drop_bomb(self) -> None:
        if self.bombs < 1:
            return

        self.bombs -= 1
        self.last_bomb_at = get_ticks()
        self.next_bomb_at = self.calculate_next_bomb()

    def animate(self) -> None:
        curr_ticks = get_ticks()
        if curr_ticks - self.last_frame_change >= self.anim_interval:
            self.curr_frame = (self.curr_frame + 1) % self.total_frames
            self.last_frame_change = curr_ticks

    def draw(self, viewpoint: Rect) -> None:
        if not viewpoint.overlaps(self.rect):
            return

        # Sprite
        self.draw_rect.x = int(self.curr_frame * self.width)
        core.video.texture_blit(
            self.texture_name,
            (
                floor(self.x - viewpoint.x),
                floor(self.y - viewpoint.y),
            ),
            self.draw_rect,
        )

        # Bomb indicator
        if self.bombs < 1:
            return

        draw_x = self.x + self.BOMBS_INDICATOR_POS[0] - viewpoint.x
        draw_y = self.y + self.BOMBS_INDICATOR_POS[1] - viewpoint.y

        for _ in range(self.bombs):
            core.video.draw_rect(
                PygameRect(draw_x, draw_y, 1, 1),
                self.BOMBS_INDICATOR_COLOR,
                1
            )
            draw_x += 2
