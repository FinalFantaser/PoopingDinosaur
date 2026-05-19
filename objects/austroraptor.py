from enum import Enum, auto
from pygame import Surface
import pygame.transform
import core.video
from objects.object import Rect, Object, Direction


class Austroraptor(Object):
    __slots__ = *Object.__slots__, "direction", "state", 'vel_x', 'vel_y', '_trigger_area'
    
    ID_STUB: str = "austroraptor_%d"
    SIZE: tuple[float, float] = 24, 8

    TEXTURE_NAME: str = "austroraptor.png"
    TEXTURE_KEY_LEFT: str = f"{TEXTURE_NAME}_{Direction.LEFT}"
    TEXTURE_KEY_RIGHT: str = f"{TEXTURE_NAME}_{Direction.RIGHT}"

    ANIM_INTERVAL: int = 125
    TOTAL_FRAMES: int = 2

    TRIGGER_AREA_SIZE: tuple[float, float] = SIZE[0] * 20, SIZE[1] * 5
    VEL_X_MIN: float = 100.0
    VEL_X_MAX: float = VEL_X_MIN * 2
    VEL_X_MAX_IN: float = 1 # Seconds to reach maximum speed
    WEIGHT: float = 300.0
    WEIGHT_FACTOR: float = 0.5
    JUMP_ACCEL: float = -(WEIGHT * 0.6)

    HANDLER_NAME: str = "AustroraptorHandler"


    _total: int = 0

    class State(Enum):
        IDLE = auto()
        STARTLED = auto()
        RUNNING = auto()
        DEAD = auto()

    def __init__(self, pos: tuple[int|float, int|float]) -> None:
        Austroraptor._total += 1
        super().__init__(
            id=self.ID_STUB % self._total,
            pos=pos,
            size=self.SIZE,
        )

        core.video.texture_load(core.paths.TEXTURES / self.TEXTURE_NAME, self.TEXTURE_KEY_RIGHT)

        if not core.video.texture_has(self.TEXTURE_KEY_LEFT):
            flipped_surf: Surface = pygame.transform.flip(
                core.video.texture_get(self.TEXTURE_KEY_RIGHT),
                *Direction.LEFT.value
            )

            flipped_surf.set_colorkey(core.video.COLOR_KEY)

            core.video.texture_add(flipped_surf, self.TEXTURE_KEY_LEFT)

        self.direction: Direction = Direction.LEFT
        self.state = self.State.IDLE
        self.vel_x: float = 0.0
        self.vel_y: float = 0.0
        self._trigger_area: Rect = Rect(*self.rect.center, *self.TRIGGER_AREA_SIZE)

    @property
    def trigger_area(self) -> Rect:
        self._trigger_area.center = self.rect.center
        return self._trigger_area

    def draw(self, viewpoint: Rect) -> None:
        if not viewpoint.overlaps(self.rect):
            return

        if self.state == Austroraptor.State.DEAD:
            core.video.texture_blit(
                f"{self.TEXTURE_NAME}_{Direction.RIGHT}",
                (self.x - viewpoint.x, self.y - viewpoint.y),
                (
                    0,
                    int(self.SIZE[1]),
                    int(self.SIZE[0]),
                    int(self.SIZE[1]),
                )
            )
        else:
            core.video.texture_blit(
                f"{self.TEXTURE_NAME}_{self.direction}",
                (self.x - viewpoint.x, self.y - viewpoint.y),
                (
                    int(self.curr_frame * self.SIZE[0]),
                    0,
                    int(self.SIZE[0]),
                    int(self.SIZE[1]),
                )
            )

    def animate(self) -> None:
        if self.vel_x == 0.0 or self.state == self.State.DEAD:
            return

        # Run animation interval is affected by dinousaur's current speed
        anim_interval: int = int(self.ANIM_INTERVAL * min(self.VEL_X_MAX/self.vel_x, 2))

        if pygame.time.get_ticks() - self.last_frame_change >= anim_interval:
            self.curr_frame = (self.curr_frame + 1) % self.TOTAL_FRAMES
            self.last_frame_change = pygame.time.get_ticks()
