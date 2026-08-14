from pygame import Rect as PygameRect
import pygame.time

import core.video
from .rect import Rect
from .dinosaur import Dinosaur, Direction

class Triceratops(Dinosaur):
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
        WEIGHT: Weight of the dinosaur.
        WEIGHT_FACTOR: Weight factor for the dinosaur physics.
        HITBOX_BITE_SIZE: Size of the area of bite.

        curr_frame: Current frame of the body.
        total_frames: Total number of frames for the body.
        anim_interval: Animation microseconds interval for the body.
        last_frame_change: Timestamp of the last frame change for the body.
        curr_frame_head: Current frame of the head.
        last_frame_change_head: Timestamp of the last frame change for the head.

    """

    __slots__ = Dinosaur.__slots__ + (
        "curr_frame_head",
        "last_frame_change_head",
    )

    HANDLER_NAME: str = "TriceratopsHandler"
    ID_STUB: str = "triceratops_%d"
    SIZE: tuple[float, float] = 38, 16
    SIZE_BODY: tuple[float, float] = 27, 16
    SIZE_HEAD: tuple[float, float] = 13, 13
    HEAD_POS: tuple[float, float] = 26, 0
    TEXTURE_NAME: str = "triceratops.png"
    ANIM_INTERVAL_HEAD: int = 100
    TOTAL_FRAMES_HEAD: int = 3
    DRAW_AREA: PygameRect = PygameRect(0, 0, *SIZE_BODY)
    DRAW_AREA_HEAD: PygameRect = PygameRect(0, 16, *SIZE_HEAD)
    FOV_SIZE = SIZE_BODY[0] * 3.5, SIZE_BODY[1]
    VEL_X_MIN: float = 175
    VEL_X_MAX: float = VEL_X_MIN * 1.3
    VEL_X_MAX_IN: float = 1
    WEIGHT: float = 5000
    WEIGHT_FACTOR: float = 0.9
    HITBOX_BITE_SIZE: tuple[float, float] = SIZE_HEAD

    def __init__(self, pos: tuple[int|float, int|float]) -> None:
        super().__init__(pos, False)
        self.direction = Direction.RIGHT
        self.state = self.State.CHASING
        self.curr_frame_head = 0
        self.last_frame_change_head = pygame.time.get_ticks()

    def draw(self, viewpoint: Rect) -> None:
        # Body
        self.DRAW_AREA.x = int(self.curr_frame * self.SIZE_BODY[0])

        core.video.texture_blit(
            self.TEXTURE_NAME,
            (self.x - viewpoint.x, self.y - viewpoint.y),
            self.DRAW_AREA
        )

        # Head
        self.DRAW_AREA_HEAD.x = int(self.curr_frame_head * self.SIZE_HEAD[0])

        core.video.texture_blit(
            self.TEXTURE_NAME,
            (
                self.x + self.HEAD_POS[0] - viewpoint.x,
                self.y + self.HEAD_POS[1] - viewpoint.y
            ),
            self.DRAW_AREA_HEAD
        )

    def animate(self) -> None:
        # Body
        super().animate()

        # Head
        if self.state == self.State.BITING:
            if pygame.time.get_ticks() - self.last_frame_change_head >= self.ANIM_INTERVAL_HEAD:
                self.last_frame_change_head = pygame.time.get_ticks()
                self.curr_frame_head = (self.curr_frame_head + 1) % self.TOTAL_FRAMES_HEAD

    @property
    def hitbox(self) -> Rect:
        """Whole body hitbox (head included)"""
        return Rect(*self.SIZE, *self.pos)

    @property
    def hitbox_body(self) -> Rect:
        """Body hitbox (no head)"""
        return Rect(*self.pos, *self.SIZE_BODY)

    @property
    def hitbox_head(self) -> Rect:
        """Head hitbox (no body)"""
        return Rect(*self.pos, *self.SIZE_HEAD)

    @property
    def hitbox_bite(self) -> Rect:
        """Bite area hitbox"""
        return Rect(self.pos[0] + self.SIZE[0], self.pos[1], *self.SIZE_HEAD)