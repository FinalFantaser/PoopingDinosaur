from typing import Self
from enum import IntEnum, auto
from pygame import Rect as PygameRect
import core.video
from objects.object import ObjectLayer, Object, Rect


class ObstacleType(IntEnum):
    CACTUS = auto(),
    THORNS = auto(),
    STONE = auto(),
    TREE = auto(),


class Obstacle(Object):
    __slots__ = *Object.__slots__, 'ob_type'

    LAYER: ObjectLayer = ObjectLayer.MAIN

    TEXTURE_NAME: str = 'obstacles.png'

    SIZES: dict[ObstacleType, tuple[float, float]] = {
        ObstacleType.CACTUS: (8, 16),
        ObstacleType.THORNS: (16, 8),
        ObstacleType.STONE: (8, 8),
        ObstacleType.TREE: (16, 16),
    }

    _ID_STUB: str = "obstacle_%d"

    _DRAW_AREAS: dict[ObstacleType, PygameRect] = {
        ObstacleType.CACTUS: PygameRect((0, 0), SIZES[ObstacleType.CACTUS]),
        ObstacleType.THORNS: PygameRect((8, 0), SIZES[ObstacleType.THORNS]),
        ObstacleType.STONE: PygameRect((24, 0), SIZES[ObstacleType.STONE]),
        ObstacleType.TREE: PygameRect((32, 0), SIZES[ObstacleType.TREE]),
    }

    _total: int = 0

    def __init__(self, ob_type: ObstacleType, pos: tuple[float, float]):
        Obstacle._total += 1

        super().__init__(
            id=self._ID_STUB % Obstacle._total,
            pos=pos,
            size=self.SIZES[ob_type],
        )

        self.ob_type: ObstacleType = ob_type

        if not core.video.texture_has(self.TEXTURE_NAME):
            core.video.texture_load(core.paths.TEXTURES / self.TEXTURE_NAME, self.TEXTURE_NAME)

    def draw(self, viewpoint: Rect) -> None:
        if not viewpoint.overlaps(self.rect):
            return

        core.video.texture_blit(
            self.TEXTURE_NAME,
            (self.x - viewpoint.x, self.y - viewpoint.y),
            self._DRAW_AREAS[self.ob_type],
        )

    @classmethod
    def place(cls, ob_type: ObstacleType, x: int|float, ground_level: int|float) -> Self:
        return cls(
            ob_type,
            (x, ground_level - cls.SIZES[ob_type][1]),
        )