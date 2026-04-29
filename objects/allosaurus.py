import pygame.time
import pygame.transform
import core.video
from objects.object import Object, Rect


class Allosaurus(Object):
    __slots__ = Object.__slots__ + ('weight', 'direction', 'vel_x', 'vel_y')

    ID: str = 'player'
    DIR_LEFT: int = -1
    DIR_RIGHT: int = 1
    TOTAL_FRAMES: int = 2
    ANIM_INTERVAL: int = 250
    SIZE: tuple[float, float] = (53, 16)
    TEXTURE_NAME: str = 'allosaurus.png'
    HANDLER_NAME: str = 'AllosaurusHandler'

    MAX_VEL_X: float = 20.0
    MAX_VEL_Y: float = 40.0
    MIN_WEIGHT: float = 1.5
    MAX_WEIGHT: float = 2.0

    def __init__(
            self,
            pos: tuple[int|float, int|float],
            direction: int = DIR_RIGHT,
            vel_x: float = 0.0,
            vel_y: float = 0.0,
    ) -> None:
        super().__init__(
            id=self.ID,
            pos=pos,
            size=self.SIZE,
            texture_name=self.TEXTURE_NAME,
            total_frames=self.TOTAL_FRAMES,
            anim_interval=self.ANIM_INTERVAL,
        )

        self.weight: float = self.MIN_WEIGHT
        self.direction: int = direction
        self.vel_x: float = vel_x
        self.vel_y: float = vel_y

    def draw(self, viewpoint: Rect) -> None:
        area: tuple[int, int, int, int] = (
            int(self.curr_frame * self.width),
            0,
            int(self.width),
            int(self.height)
        )

        surface: pygame.Surface = self.texture
        if self.direction == self.DIR_LEFT:
            surface = pygame.transform.flip(surface, True, False)

        core.video.texture_blit(
            surface,
            (self.x - viewpoint.x, self.y - viewpoint.y),
            area
        )

    def animate(self) -> None:
        if self.vel_x == 0.0:
            self.curr_frame = 0
            return

        if pygame.time.get_ticks() - self.last_frame_change >= self.ANIM_INTERVAL:
            self.last_frame_change = pygame.time.get_ticks()
            self.curr_frame += 1
            if self.curr_frame >= self.TOTAL_FRAMES:
                self.curr_frame = 0