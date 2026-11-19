from math import floor
import core.video
from .rect import Rect
from .object_with_physics import ObjectWithPhysics


class Bomb(ObjectWithPhysics):
    __slots__ = (
		*ObjectWithPhysics.__slots__,
        # Your slots here ...
    )

    HANDLER_NAME: str = "BombHandler"
    ID_STUB: str = "bomb_%d"
    TEXTURE_NAME: str = "bomb.png"
    WIDTH: float = 8
    HEIGHT: float = 5
    SIZE: tuple[float, float] = WIDTH, HEIGHT
    TOTAL_FRAMES: int = 1
    ANIM_INTERVAL: int = 0
    X_SLOWDOWN_RATE: float = 175 / 500

    _total: int = 0

    def __init__(self, pos: tuple[float, float] = (0, 0), vel_x: float = 0):
        Bomb._total += 1

        super().__init__(
            id=self.ID_STUB % self._total,
            pos=pos,
            size=self.SIZE,
            texture_name=self.TEXTURE_NAME,
            total_frames=self.TOTAL_FRAMES,
            anim_interval=self.ANIM_INTERVAL,
        )

        self.vel_x = vel_x

    def draw(self, viewpoint: Rect) -> None:
        core.video.texture_blit(
            self.texture_name,
            (
                floor(self.x - viewpoint.x),
                floor(self.y - viewpoint.y),
            )
        )