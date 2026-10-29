from enum import IntEnum
from random import choice
from math import floor

import pygame.transform
from pygame import Rect as PygameRect, Surface
from pygame.time import get_ticks
from pygame.math import Vector2
import core.video
from .object import Object
from .layer import Layer
from .direction import Direction



class Skyscraper(Object):
    __slots__ = (
		*Object.__slots__,
        "pivot",
        "offset",
        "angle",
        "invincibility",
        "health",
        "texture_rotated",
    )

    ID_STUB: str = "skyscraper_%d"
    HANDLER_NAME: str = "SkyscraperHandler"
    TEXTURE_NAME: str = "skyscraper.png"
    MAX_HEALTH: tuple[int, int] = 1, 2
    MAX_INVINCIBILITY: int = 1000
    MAX_ANGLE: float = -90
    SIZE: tuple[tuple[float, float], tuple[float, float]] = (16, 60), (16, 100)
    TOTAL_FRAMES: int = 1
    ANIM_INTERVAL: int = 0

    total: int = 0

    class Type(IntEnum):
        LOW = 0
        TALL = 1

    def __init__(self, pos: tuple[float, float] = (0, 0), type: Type|None = None):
        self.total += 1
        self.type: Skyscraper.Type = type if type is not None else choice((self.Type.LOW, self.Type.TALL))

        super().__init__(
            id=self.ID_STUB % self.total,
            pos=pos,
            texture_name=self.TEXTURE_NAME,
            total_frames=self.TOTAL_FRAMES,
            anim_interval=self.ANIM_INTERVAL
        )

        self.angle: float = 0
        self.pivot: Vector2 = Vector2(self.rect.center_x, 0)
        self.offset: Vector2 = Vector2(0, -self.height / 2)
        self.invincibility: int = 0
        self.health: int = self.MAX_HEALTH[self.type.value]

        self.texture_rotated = self.texture.copy()

    def rotate(self, angle_change: float) -> None:
        self.angle += angle_change

        new_center = self.pivot + self.offset.rotate(self.angle)

        self.texture_rotated = Surface(self.SIZE[self.Type.TALL])
        self.texture_rotated.fill(core.video.COLOR_KEY)
        self.texture_rotated.set_colorkey(core.video.COLOR_KEY)
        self.texture_rotated.blit(
            core.video.texture_get(self.TEXTURE_NAME),
            (0, 0),
            (self.type.value * self.width, 0, self.SIZE[self.Type.TALL])
        )

        self.texture_rotated = pygame.transform.rotate(self.texture_rotated, self.angle)
        self.rect = self.texture_rotated.get_rect(center=new_center)

