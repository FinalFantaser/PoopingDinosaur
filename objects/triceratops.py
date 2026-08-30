from pygame import Rect as PygameRect
import pygame.time

import core.video
from .rect import Rect
from .separate_head_dinosaur import SeparateHeadDinosaur, Direction

class Triceratops(SeparateHeadDinosaur):
    """
    Attributes:
        ID_STUB: Stub for a dinosaur.
        SIZE: Overall size of the triceratops
        SIZE_BODY: Body size of the triceratops.
        SIZE_HEAD: Head size of the triceratops.
        TEXTURE_NAME: Name of a texture used.
        ANIM_INTERVAL: Animation interval for the body (microseconds).
        ANIM_INTERVAL_HEAD: Animation interval for the head (microseconds).
        TOTAL_FRAMES: Total number of frames.
        DRAW_AREA: Texture area of the triceratops body.
        DRAW_AREA_HEAD: Texture area of the triceratops head.
        VEL_X_MIN: Minimum velocity of a dinosaur.
        VEL_X_MAX: Maximum velocity of a dinosaur.
        VEL_X_MAX_IN: Time to reach maximum velocity (seconds).
        WEIGHT: Weight of the dinosaur (kg).
        WEIGHT_FACTOR: Weight factor for the dinosaur physics.
        HITBOX_BITE_SIZE: Size of the area of bite.

        curr_frame: Current frame of the body.
        total_frames: Total number of frames for the body.
        anim_interval: Animation microseconds interval for the body.
        last_frame_change: Timestamp of the last frame change for the body.
        curr_frame_head: Current frame of the head.
        last_frame_change_head: Timestamp of the last frame change for the head.

    """

    HANDLER_NAME: str = "TriceratopsHandler"
    ID_STUB: str = "triceratops_%d"
    SIZE: tuple[float, float] = 38, 16
    SIZE_BODY: tuple[float, float] = 27, 16
    SIZE_HEAD: tuple[float, float] = 13, 13
    HEAD_POS: tuple[float, float] = 26, 0
    TEXTURE_NAME: str = "triceratops.png"
    ANIM_INTERVAL_HEAD: int = 200
    TOTAL_FRAMES_HEAD: int = 3
    DRAW_AREA: PygameRect = PygameRect(0, 0, *SIZE_BODY)
    DRAW_AREA_HEAD: PygameRect = PygameRect(0, 16, *SIZE_HEAD)
    FOV_SIZE = SIZE_BODY[0] * 3.5, SIZE_BODY[1]
    VEL_X_MIN: float = 175
    VEL_X_MAX: float = VEL_X_MIN * 1.3
    VEL_X_MAX_IN: float = 1
    WEIGHT: float = 5000
    WEIGHT_FACTOR: float = 0.9
    HEALTH_MAX: int = 3
    HITBOX_BITE_SIZE: tuple[float, float] = SIZE_HEAD

    def __init__(self, pos: tuple[float, float]) -> None:
        super().__init__(pos)
        self.state = self.State.CHASING
