from random import randint
from math import floor
from pygame import Rect as PygameRect
from pygame.transform import flip
from pygame.time import get_ticks
import core.video
from .direction import Direction
from .rect import Rect
from .layer import Layer
from .object import Object
from .human import Human


class Soldier(Human):
    __slots__ = (
		*Human.__slots__,
        "next_shot_at",
    )

    HANDLER_NAME: str = "SoldierHandler"
    ID_STUB: str = "soldier_%s"
    TEXTURE_NAME: str = "soldier.png"
    SHOOT_INTERVAL: tuple[int, int] = 500, 1000
    DRAW_Y_STATES: dict[int, int] = {
        Human.State.IDLE.value: 0,
        Human.State.STARTLED.value: 0,
        Human.State.RUNNING.value: 1,
        Human.State.SHOOTING.value: 2,
    }
    TEXTURE_DIR_KEYS: dict[int, str] = {
        Direction.RIGHT.value[0]: TEXTURE_NAME,
        Direction.LEFT.value[0]: f"{TEXTURE_NAME}_left",
    }

    _total: int = 0
    _cached: bool = False

    def __init__(
            self,
            pos: tuple[float, float] = (0, 0),
            state: Human.State = Human.State.IDLE,
            direction: Direction = Direction.LEFT,
    ) -> None:
        Soldier._total += 1

        super().__init__(
            id=self.ID_STUB % self._total,
            texture_name=self.TEXTURE_NAME,
            pos=pos,
            state=state,
            direction=direction,
        )

        self.next_shot_at: int = get_ticks() + randint(*self.SHOOT_INTERVAL)

        if not self._cached:
            self._cache()

    def animate(self) -> None:
        if self.state == self.State.IDLE or self.state == self.State.STARTLED:
            return

        curr_ticks = get_ticks()
        if curr_ticks - self.last_frame_change >= self.anim_interval:
            self.curr_frame = (self.curr_frame + 1) % self.total_frames
            self.last_frame_change = curr_ticks

    def draw(self, viewpoint: Rect) -> None:
        if not viewpoint.overlaps(self.rect):
            return

        self.draw_rect.x = int(self.curr_frame * self.width)
        self.draw_rect.y = int(self.DRAW_Y_STATES[self.state.value] * self.height)

        core.video.texture_blit(
            self.TEXTURE_DIR_KEYS[self.direction.value[0]],
            (
                floor(self.x - viewpoint.x),
                floor(self.y - viewpoint.y),
            ),
            self.draw_rect,
        )

    def _cache(self) -> None:
        flipped_texture = flip(self.texture, *Direction.LEFT.value)
        flipped_texture.set_colorkey(core.video.COLOR_KEY)

        core.video.texture_add(
            flipped_texture,
            self.TEXTURE_DIR_KEYS[Direction.LEFT.value[0]],
        )

        Soldier._cached = True