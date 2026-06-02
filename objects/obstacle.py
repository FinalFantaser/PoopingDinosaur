from typing import Self
from enum import IntEnum, auto
from pygame import Rect as PygameRect
import core.video
from objects.object import Object, Rect


class Obstacle(Object):
    __slots__ = *Object.__slots__, "ob_type"

    class Type(IntEnum):
        CACTUS = auto(),
        THORNS = auto(),
        STONE = auto(),
        TREE = auto(),


    LAYER: Object.Layer = Object.Layer.MAIN
    TEXTURE_NAME: str = "obstacles.png"
    HANDLER_NAME = "ObstacleHandler"

    SIZES: dict[Type, tuple[float, float]] = {
        Type.CACTUS: (8, 16),
        Type.THORNS: (16, 8),
        Type.STONE: (8, 8),
        Type.TREE: (16, 16),
    }

    _ID_STUB: str = "obstacle_%d"

    _DRAW_AREAS: dict[Type, PygameRect] = {
        Type.CACTUS: PygameRect(0, 0, *SIZES[Type.CACTUS]),
        Type.THORNS: PygameRect(8, 8, *SIZES[Type.THORNS]),
        Type.STONE: PygameRect(24, 8, *SIZES[Type.STONE]),
        Type.TREE: PygameRect(32, 0, *SIZES[Type.TREE]),
    }

    _total: int = 0

    def __init__(self, ob_type: Type, pos: tuple[float, float]):
        Obstacle._total += 1

        super().__init__(
            id=self._ID_STUB % Obstacle._total,
            pos=pos,
            size=self.SIZES[ob_type],
        )

        self.ob_type: Type = ob_type

        if not core.video.texture_has(self.TEXTURE_NAME):
            core.video.texture_load(core.paths.TEXTURES / self.TEXTURE_NAME, self.TEXTURE_NAME)

    def draw(self, viewpoint: Rect) -> None:
        if not viewpoint.overlaps(self.rect):
            return

        core.video.texture_blit(
            self.TEXTURE_NAME,
            (self.x - viewpoint.x, self.y - viewpoint.y),
            self._DRAW_AREAS[self.ob_type]
        )