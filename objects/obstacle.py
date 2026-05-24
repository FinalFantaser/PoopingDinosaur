from enum import IntEnum, auto
from pygame import Rect as PygameRect
import core.video
from objects.object import ObjectLayer, Object, Rect


class ObstacleType(IntEnum):
    CACTUS = auto(),


class Obstacle(Object):
    __slots__ = *Object.__slots__, 'ob_type'

    LAYER: ObjectLayer = ObjectLayer.MAIN

    TEXTURE_NAME: str = 'obstacles.png'

    _ID_STUB: str = "obstacle_%d"

    _SIZES: dict[ObstacleType, tuple[float, float]] = {
        ObstacleType.CACTUS: (8, 16),
        # ...
    }

    _DRAW_AREAS: dict[ObstacleType, PygameRect] = {
        ObstacleType.CACTUS: PygameRect((0, 0), _SIZES[ObstacleType.CACTUS]),
    }

    _total: int = 0

    def __init__(self, ob_type: ObstacleType, pos: tuple[float, float]):
        Obstacle._total += 1

        super().__init__(
            id=self._ID_STUB % Obstacle._total,
            pos=pos,
            size=self._SIZES[ob_type],
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
        )