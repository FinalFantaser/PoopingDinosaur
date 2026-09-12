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

    def draw_body(self, viewpoint: Rect) -> None:
        texture_offset_y = max(0, self.direction.value[0]) * self.SIZE_BODY[1]

        draw_area_x = int(self.curr_frame * self.SIZE_BODY[0])
        draw_area_y = int(self.DRAW_AREA[1] + texture_offset_y)

        body_rect = self.rect_body

        core.video.texture_blit(
            self.TEXTURE_NAME,
            (body_rect.x - viewpoint.x, body_rect.y - viewpoint.y),
            (draw_area_x, draw_area_y, self.DRAW_AREA.width, self.DRAW_AREA.height),
        )

    def draw_head(self, viewpoint: Rect) -> None:
        texture_offset_y = max(0, self.direction.value[0]) * self.SIZE_HEAD[1]

        head_rect = self.rect_head

        dest_x = head_rect.x - viewpoint.x
        dest_y = head_rect.y - viewpoint.y

        draw_area_x = int(self.curr_frame_head * self.SIZE_HEAD[0])
        draw_area_y = int(self.DRAW_AREA_HEAD[1] + texture_offset_y)

        core.video.texture_blit(
            self.TEXTURE_NAME,
            (dest_x, dest_y),
            (draw_area_x, draw_area_y, self.DRAW_AREA_HEAD.width, self.DRAW_AREA_HEAD.height),
        )

    def draw(self, viewpoint: Rect) -> None:
        if not viewpoint.overlaps(self.rect):
            return

        self.draw_body(viewpoint)
        self.draw_head(viewpoint)

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
    def rect_body(self) -> Rect:
        rect = self.rect

        body = Rect(rect.x, rect.y, self.SIZE_BODY[0], self.SIZE_BODY[1])

        return body

    @property
    def rect_head(self) -> Rect:
        body_rect = self.rect_body

        head = Rect(
            (body_rect.right + self.HEAD_POS[0]) if self.direction == Direction.RIGHT else (body_rect.left - self.SIZE_HEAD[0] - self.HEAD_POS[0]),
            self.y + self.HEAD_POS[1],
            *self.SIZE_HEAD
        )

        return head

    @property
    def hitbox_body(self) -> Rect:
        """Body hitbox (no head)"""
        return self.rect_body

    @property
    def hitbox_head(self) -> Rect:
        """Head hitbox (no body)"""
        return self.rect_head

    @property
    def hitbox_bite(self) -> Rect:
        """Bite area hitbox"""
        return self.hitbox_head

    def die(self) -> None:
        super().die()
        self.curr_frame_head = 0
        self.last_frame_change_head = get_ticks()