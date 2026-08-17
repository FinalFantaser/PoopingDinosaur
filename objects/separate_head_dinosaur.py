from pygame import Rect as PygameRect
from pygame.time import get_ticks

import core.video
from .rect import Rect
from .dinosaur import Dinosaur, Direction


class SeparateHeadDinosaur(Dinosaur):
    """
    Basic class for a dinosaur with individually controlled head
    """

    __slots__ = Dinosaur.__slots__ + (
        "curr_frame_head",
        "last_frame_change_head",
    )

    SIZE_BODY: tuple[float, float] = 0, 0
    SIZE_HEAD: tuple[float, float] = 0, 0
    HEAD_POS: tuple[float, float] = 0, 0
    ANIM_INTERVAL_HEAD: int = 100
    TOTAL_FRAMES_HEAD: int = 3
    DRAW_AREA: PygameRect = PygameRect(0, 0, *SIZE_BODY)
    DRAW_AREA_HEAD: PygameRect = PygameRect(0, 16, *SIZE_HEAD)
    HITBOX_BITE_SIZE: tuple[float, float] = SIZE_HEAD

    def __init__(self, pos: tuple[int|float, int|float], flippable: bool = False) -> None:
        super().__init__(pos, flippable)
        self.direction = Direction.RIGHT
        self.curr_frame_head = 0
        self.last_frame_change_head = get_ticks()

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
        if self.state == self.State.DEAD:
            return

        # Body
        super().animate()

        # Head
        if self.state == self.State.BITING:
            if get_ticks() - self.last_frame_change_head >= self.calc_anim_interval(self.ANIM_INTERVAL_HEAD):
                self.last_frame_change_head = get_ticks()
                self.curr_frame_head = (self.curr_frame_head + 1) % self.TOTAL_FRAMES_HEAD

    @property
    def hitbox(self) -> Rect:
        """Whole body hitbox (head included)"""
        return Rect(*self.pos, *self.SIZE)

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