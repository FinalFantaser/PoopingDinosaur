from math import floor
from pygame import Rect as PygameRect
from pygame.time import get_ticks
from pygame import transform
import core.video
import core.paths
from .rect import Rect
from .object import Object


class Missile(Object):
    __slots__ = (
        *Object.__slots__,
        "vel_x", "vel_y",
        "angle",
        "target_id",
        "_hitbox",
    )

    HANDLER_NAME: str = "MissileHandler"
    ID_STUB: str = "missile_%d"
    TEXTURE_NAME: str = "missile.png"
    WIDTH: float = 12
    HEIGHT: float = 7
    SIZE: tuple[float, float] = WIDTH, HEIGHT
    TOTAL_FRAMES: int = 2
    ANIM_INTERVAL: int = 250
    SPEED: float = 250
    ROTATION_SPEED: float = 180

    _total: int = 0

    # Cached texture data
    _cached: bool = False
    _cached_sizes: dict[
        int,
        tuple[
            tuple[float, float],
            tuple[float, float],
        ]
    ] = {}

    def __init__(self, pos: tuple[float, float] = (0, 0), angle: float = 0, target_id: str|None = None) -> None:
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
        self.target_id: str|None = target_id
        self._hitbox: Rect = self.rect.get_copy()

        if not Missile._cached:
            self.cache_textures()

    @property
    def curr_size(self) -> tuple[float, float]:
        return self._cached_sizes[int(self.angle) % 360][self.curr_frame]

    @property
    def hitbox(self) -> Rect:
        self._hitbox.size = self.curr_size
        self._hitbox.center = self.rect.center
        return self._hitbox

    def animate(self) -> None:
        curr_ticks = get_ticks()

        if curr_ticks - self.last_frame_change >= self.anim_interval:
            self.last_frame_change = curr_ticks
            self.curr_frame = (self.curr_frame + 1) % self.total_frames

    def draw(self, viewpoint: Rect) -> None:
        box = self.hitbox
        if not viewpoint.overlaps(box):
            return

        degree = int(self.angle) % 360
        key = f"{self.texture_name}_{degree}_{self.curr_frame}"
        core.video.texture_blit(
            key,
            (
                floor(box.x - viewpoint.x),
                floor(box.y - viewpoint.y)
            ),
        )

        # For debugging purposes
        # hitbox = self.hitbox.to_pygame_rect()
        # hitbox.x -= viewpoint.x
        # hitbox.y -= viewpoint.y
        #
        # core.video.draw_rect(
        #     hitbox,
        #     "0xFF0000",
        #     1
        # )

    @classmethod
    def cache_textures(cls) -> None:
        if cls._cached:
            return

        src_surf = core.video.texture_load(core.paths.TEXTURES / cls.TEXTURE_NAME, cls.TEXTURE_NAME)
        frames = tuple(src_surf.subsurface(frame * cls.WIDTH, 0, *cls.SIZE) for frame in range(cls.TOTAL_FRAMES))

        for modifier in -1, 1:
            for degree in range(min(0, 360 * modifier), max(0, 361 * modifier)):
                sizes = []
                for frame_num in range(cls.TOTAL_FRAMES):
                    rotated_surf = transform.rotate(frames[frame_num], 180 - degree)
                    sizes.append(rotated_surf.get_size())

                    core.video.texture_add(
                        rotated_surf,
                        f"{cls.TEXTURE_NAME}_{degree}_{frame_num}"
                    )

                cls._cached_sizes[degree] = tuple(sizes)

        cls._cached = True