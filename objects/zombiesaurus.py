from math import floor
from pygame import Rect as PygameRect
from pygame.time import get_ticks
import core.video
from . import Rect
from .object import Object
from .layer import Layer
from .direction import Direction
from .separate_head_dinosaur import SeparateHeadDinosaur


class Zombiesaurus(SeparateHeadDinosaur):
    __slots__ = (
		*SeparateHeadDinosaur.__slots__,
        "emerge_progress",
    )

    HANDLER_NAME: str = "ZombiesaurusHandler"
    ID_STUB: str = "zombiesaurus_%d"
    TEXTURE_NAME: str = "zombiesaurus.png"
    WIDTH: float = 40
    HEIGHT: float = 14
    SIZE: tuple[float, float] = WIDTH, HEIGHT
    SIZE_BODY: tuple[float, float] = 31, 14
    SIZE_HEAD: tuple[float, float] = 11, 11
    HEAD_POS: tuple[float, float] = -2, 0
    ANIM_INTERVAL: int = 250
    TOTAL_FRAMES: int = 2
    ANIM_INTERVAL_HEAD: int = 100
    TOTAL_FRAMES_HEAD: int = 3
    DRAW_AREA: PygameRect = PygameRect(0, 0, *SIZE_BODY)
    DRAW_AREA_HEAD: PygameRect = PygameRect(0, 28, *SIZE_HEAD)
    HITBOX_BITE_SIZE: tuple[float, float] = SIZE_HEAD
    WEIGHT: float = 1500
    WEIGHT_FACTOR: float = 0.8
    JUMP_ACCEL: float = -(WEIGHT * 8)

    EMERGE_TIME: int = 500
    EMERGE_PER_MS: float = HEIGHT / EMERGE_TIME


    def __init__(self, pos: tuple[float, float] = (0, 0)):
        super().__init__(pos)
        self.state = self.State.IDLE
        self.emerge_progress: float = self.EMERGE_TIME

    def draw_body(self, viewpoint: Rect) -> None:
        """IDLE state is for the emerging phase"""
        if self.state != self.State.IDLE:
            super().draw_body(viewpoint)
            return

        texture_offset_y = max(0, self.direction.value[0]) * self.SIZE_BODY[1]
        y_diff = self.emerge_progress * self.EMERGE_PER_MS

        draw_area = Rect.from_pygame_rect(self.DRAW_AREA)

        draw_area.x = self.curr_frame * self.WIDTH
        draw_area.y = self.DRAW_AREA[1] + texture_offset_y

        draw_area.height -= y_diff

        core.video.texture_blit(
            self.TEXTURE_NAME,
            (
                floor(self.x - viewpoint.x),
                floor(self.y + y_diff - viewpoint.y)
            ),
            draw_area.to_pygame_rect()
        )

    def draw_head(self, viewpoint) -> None:
        """IDLE state is for the emerging phase"""
        if self.state != self.State.IDLE:
            super().draw_head(viewpoint)

        if self.emerge_progress <= 0:
            return

        texture_offset_y = max(0, self.direction.value[0]) * self.SIZE_HEAD[1]
        y_diff = self.emerge_progress * self.EMERGE_PER_MS

        draw_area = Rect.from_pygame_rect(self.DRAW_AREA_HEAD)
        draw_area.x = self.curr_frame_head * self.WIDTH
        draw_area.y = self.DRAW_AREA_HEAD[1] + texture_offset_y

        head_rect = self.rect_head.get_copy()
        head_rect.y += y_diff

        if head_rect.bottom >= self.rect.bottom:
            head_y_diff = head_rect.bottom - self.rect.bottom
            draw_area.height -= head_y_diff

        core.video.texture_blit(
            self.TEXTURE_NAME,
            (
                floor(head_rect.x - viewpoint.x),
                floor(head_rect.y - viewpoint.y)
            ),
            draw_area.to_pygame_rect()
        )
