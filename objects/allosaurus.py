import core.video

from pygame import Rect as PygameRect
from .separate_head_dinosaur import Rect, SeparateHeadDinosaur, Direction

class Allosaurus(SeparateHeadDinosaur):
    HANDLER_NAME: str = 'AllosaurusHandler'
    ID_STUB: str = "allosaurus_%d"
    SIZE: tuple[float, float] = 37, 13
    SIZE_BODY: tuple[float, float] = 29, 13
    SIZE_HEAD: tuple[float, float] = 9, 9
    TEXTURE_NAME: str = "allosaurus.png"
    HEAD_POS: tuple[float, float] = 0, 0
    DRAW_AREA: PygameRect = PygameRect(0, 0, *SIZE_BODY)
    DRAW_AREA_HEAD: PygameRect = PygameRect(0, 26, *SIZE_HEAD)
    FOV_SIZE: tuple[float, float] = SIZE[0] * 4, SIZE[1]
    VEL_X_MIN: float = 150
    VEL_X_MAX: float = VEL_X_MIN * 1.5
    VEL_X_MAX_IN: float = 1
    WEIGHT: float = 1750
    WEIGHT_FACTOR: float = 0.7
    JUMP_ACCEL = -WEIGHT * 0.1
    HEALTH_MAX: int = 2
    HITBOX_BITE_SIZE: tuple[float, float] = SIZE_HEAD

    _total: int = 0

    def __init__(self, pos: tuple[float, float] = (0, 0), direction: Direction = Direction.LEFT) -> None:
        super().__init__(pos, flippable=False)
        self.direction = direction