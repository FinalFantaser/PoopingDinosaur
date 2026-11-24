from random import randint
from math import floor
from pygame import Rect as PygameRect
from pygame.time import get_ticks
import core.video
from .rect import Rect
from .object_with_physics import ObjectWithPhysics


class Jeep(ObjectWithPhysics):
    HANDLER_NAME: str = "JeepHandler"
    ID_STUB: str = "jeep_%d"
    TEXTURE_NAME: str = "jeep.png"
    WIDTH: float = 16
    HEIGHT: float = 17
    SIZE: tuple[float, float] = WIDTH, HEIGHT
    TOTAL_FRAMES: int = 2
    ANIM_INTERVAL: int = 150
    VEL_X: float = -150
    SHOOT_INTERVAL: tuple[int, int] = 500, 1500
    _total: int = 0

    __slots__ = (
		*ObjectWithPhysics.__slots__,
        "next_shot_at",
        "draw_rect",
    )

    def __init__(self, pos: tuple[float, float] = (0, 0)) -> None:
        Jeep._total += 1

        super().__init__(
            id=self.ID_STUB % self._total,
            pos=pos,
            size=self.SIZE,
            texture_name=self.TEXTURE_NAME,
            total_frames=self.TOTAL_FRAMES,
            anim_interval=self.ANIM_INTERVAL,
        )

        self.vel_x = self.VEL_X
        self.next_shot_at: int = get_ticks() + randint(*self.SHOOT_INTERVAL)
        self.draw_rect: PygameRect = PygameRect(0, 0, *self.size)

    @property
    def hitbox(self) -> Rect:
        return self.rect

    def animate(self) -> None:
        curr_ticks = get_ticks()
        if curr_ticks - self.last_frame_change >= self.anim_interval:
            self.curr_frame = (self.curr_frame + 1) % self.total_frames
            self.last_frame_change = curr_ticks

    def draw(self, viewpoint: Rect) -> None:
        if not viewpoint.overlaps(self.rect):
            return

        self.draw_rect.x = int(self.curr_frame * self.width)

        core.video.texture_blit(
            self.texture_name,
            (
                floor(self.x - viewpoint.x),
                floor(self.y - viewpoint.y),
            ),

            self.draw_rect,
        )