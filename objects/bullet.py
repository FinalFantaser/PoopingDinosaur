from math import floor
from pygame import Rect as PygameRect
from pygame.time import get_ticks
import core.video
from .direction import Direction
from .rect import Rect
from .layer import Layer
from .object import Object



class Bullet(Object):
    __slots__ = (
		*Object.__slots__,
        "direction",
    )

    HANDLER_NAME: str = "BulletHandler"
    ID_STUB: str = "bullet_%d"
    TEXTURE_NAME: str = "bullet.png"
    WIDTH: float = 3
    HEIGHT: float = 3
    SIZE: tuple[float, float] = WIDTH, HEIGHT
    TOTAL_FRAMES: int = 1
    ANIM_INTERVAL: int = 0
    VEL_X: float = 300

    _total: int = 0

    def __init__(self, pos: tuple[float, float] = (0, 0), direction: Direction = Direction.LEFT):
        Bullet._total += 1

        super().__init__(
            id=self.ID_STUB % self._total,
            pos=pos,
            size=self.SIZE,
            texture_name=self.TEXTURE_NAME,
            total_frames=self.TOTAL_FRAMES,
            anim_interval=self.ANIM_INTERVAL,
        )

        self.direction: Direction = direction

    def draw(self, viewpoint: Rect) -> None:
        if not viewpoint.overlaps(self.rect):
            return

        core.video.texture_blit(
            self.texture_name,
            (
                floor(self.x - viewpoint.x),
                floor(self.y - viewpoint.y)
            )
        )