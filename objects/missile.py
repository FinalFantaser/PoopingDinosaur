from math import floor
from pygame import Rect as PygameRect
from pygame.time import get_ticks
from pygame import transform
import core.video
from .direction import Direction
from .rect import Rect
from .layer import Layer
from .object import Object


class Missile(Object):
    __slots__ = (
        *Object.__slots__,
        "vel_x", "vel_y",
        "angle",
        "target_id",
    )

    HANDLER_NAME: str = "MissileHandler"
    ID_STUB: str = "missile_%d"
    TEXTURE_NAME: str = "missile.png"
    WIDTH: float = 4
    HEIGHT: float = 8
    SIZE: tuple[float, float] = WIDTH, HEIGHT
    TOTAL_FRAMES: int = 2
    ANIM_INTERVAL: int = 250
    SPEED: float = 300
    ROTATION_SPEED: float = 180

    _total: int = 0
    _cached: bool = False

    def __init__(self, pos: tuple[float, float], angle: float = 0, target: str|None = None) -> None:
        Missile._total += 1

        super().__init__(
            id=self.ID_STUB % self._total,
            pos=pos,
            size=self.SIZE,
            texture_name=self.TEXTURE_NAME,
            total_frames=self.TOTAL_FRAMES,
            anim_interval=self.ANIM_INTERVAL,
        )

        self.vel_x: float = 0
        self.vel_y: float = 0
        self.angle: float = angle
        self.target: str|None = target

        if Missile._cached:
            return

        # Caching rotation textures
        src_surf = core.video.texture_get(self.texture_name)
        frames = tuple(src_surf.subsurface(frame * self.width, 0, *self.size) for frame in range(self.total_frames))

        for degree in range(361):
            for frame_num in range(self.total_frames):
                rotated_surface = transform(frames[frame_num], degree)
                key = f"{self.texture_name}_{degree}_{frame_num}"
                core.video.texture_add(rotated_surface, key, True)

        Missile._cached = True

    def draw(self, viewpoint: Rect) -> None:
        if not viewpoint.overlaps(self.rect):
            return

        key = f"{self.texture_name}_{int(self.angle)}_{self.curr_frame}"

        core.video.texture_blit(
            key,
            (
                floor(self.x - viewpoint.x),
                floor(self.y - viewpoint.y),
            )
        )
