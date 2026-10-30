from enum import IntEnum
from random import choice
from math import floor

from pygame import transform, Mask
from pygame.mask import from_surface as mask_from_surface
from pygame import Rect as PygameRect, Surface
from pygame.time import get_ticks

import core.video
from .rect import Rect
from .object import Object



class Skyscraper(Object):
    """
    Attributes:
        type: Type of the building (TALL or LOW)
        angle: Current rotation angle
        invincibility: Time period when the skyscraper is resistant to impacts.
        health: Remaining durability
        texture_rotated: Currently transformed (rotated) texture
        bit_mask: Mask for pixel-perfect collision check
    """
    __slots__ = (
		*Object.__slots__,
        "type",
        "angle",
        "invincibility",
        "health",
        "texture_rotated",
        "bit_mask",
    )

    ID_STUB: str = "skyscraper_%d"
    HANDLER_NAME: str = "SkyscraperHandler"
    TEXTURE_NAME: tuple[str, str] = "skyscraper_low.png", "skyscraper_high.png"
    MAX_HEALTH: tuple[int, int] = 1, 2
    MAX_INVINCIBILITY: int = 1000
    MAX_ANGLE: float = -90
    DEGREES_PER_MS: float = MAX_ANGLE / 1000
    SIZE: tuple[tuple[float, float], tuple[float, float]] = (16, 60), (16, 100)
    TOTAL_FRAMES: int = 1
    ANIM_INTERVAL: int = 0

    total: int = 0

    class Type(IntEnum):
        LOW = 0
        TALL = 1

    def __init__(self, pos: tuple[float, float] = (0, 0), type: Type|None = None):
        Skyscraper.total += 1
        self.type: Skyscraper.Type = type if type is not None else choice((self.Type.LOW, self.Type.TALL))

        super().__init__(
            id=self.ID_STUB % self.total,
            pos=pos,
            size=self.SIZE[self.type.value],
            texture_name=self.TEXTURE_NAME[self.type.value],
            total_frames=self.TOTAL_FRAMES,
            anim_interval=self.ANIM_INTERVAL
        )

        self.angle: float = 0
        self.invincibility: int = 0
        self.health: int = self.MAX_HEALTH[self.type.value]

        self.texture_rotated: Surface = self.texture.copy()
        self.texture_rotated.set_colorkey(core.video.COLOR_KEY)
        self.bit_mask: Mask = mask_from_surface(self.texture_rotated)

    def rotate(self, angle_change: float) -> None:
        if angle_change >= 0:
            return

        self.angle = max(self.MAX_ANGLE, self.angle + angle_change)
        self.texture_rotated = transform.rotate(self.texture, self.angle)
        self.texture_rotated.set_colorkey(core.video.COLOR_KEY)
        self.bit_mask: Mask = mask_from_surface(self.texture_rotated)

    def draw(self, viewpoint: Rect) -> None:
        curr_width, curr_height = self.texture_rotated.get_size()

        diff_h = self.height - curr_height

        dest_x = floor(self.x - viewpoint.x)
        dest_y = floor(self.y + diff_h - viewpoint.y)

        core.video.texture_blit(self.texture_rotated, (dest_x, dest_y))

    @property
    def max_health(self) -> int:
        return self.MAX_HEALTH[self.type.value]

    @property
    def rect_rotated(self) -> Rect:
        curr_width, curr_height = self.texture_rotated.get_size()
        diff_w, diff_h = self.width - curr_width, self.height - curr_height

        return Rect(self.x + diff_w, self.y + diff_h, curr_width, curr_height)