import core.video

from pygame import Rect as PygameRect
from .separate_head_dinosaur import Rect, SeparateHeadDinosaur

class Allosaurus(SeparateHeadDinosaur):
    HANDLER_NAME: str = 'AllosaurusHandler'
    ID_STUB: str = "allosaurus_%d"
    SIZE: tuple[float, float] = 37, 13
    SIZE_BODY: tuple[float, float] = 29, 13
    SIZE_HEAD: tuple[float, float] = 9, 9
    TEXTURE_NAME: str = "allosaurus.png"
    HEAD_POS: tuple[float, float] = 28, 0
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

    def __init__(self, pos: tuple[float, float] = (0, 0)) -> None:
        super().__init__(pos, flippable=False)

    def draw(self, viewpoint: Rect) -> None:
        if not viewpoint.overlaps(self.rect):
            return

        # Body
        offset = self.direction.value[0] * self.TOTAL_FRAMES * self.SIZE_BODY[0]
        self.DRAW_AREA.x = int(self.curr_frame * self.SIZE_BODY[0]) + offset

        core.video.texture_blit(
            self.TEXTURE_NAME,
            (self.x - viewpoint.x, self.y - viewpoint.y),
            self.DRAW_AREA
        )

        # Head
        offset = self.direction.value[0] * self.TOTAL_FRAMES * self.SIZE_HEAD[0]
        self.DRAW_AREA_HEAD.x = int(self.curr_frame_head * self.SIZE_HEAD[0]) + offset

        core.video.texture_blit(
            self.TEXTURE_NAME,
            (
                self.x + self.HEAD_POS[0] - viewpoint.x,
                self.y + self.HEAD_POS[1] - viewpoint.y
            ),
            self.DRAW_AREA_HEAD
        )