import pygame.time
import core.video
from objects.object import Object, Rect


class Allosaurus(Object):
    __slots__ = Object.__slots__ + ('direction', 'vel_x', 'vel_y')

    DIR_LEFT: int = -1
    DIR_RIGHT: int = 1
    TOTAL_FRAMES: int = 2
    ANIM_INTERVAL: int = 250
    SIZE: tuple[float, float] = (53, 16)
    TEXTURE_NAME: str = 'allosaurus.png'

    def __init__(
            self,
            id: str,
            pos: tuple[int|float, int|float],
            direction: int = DIR_RIGHT,
            vel_x: float = 0.0,
            vel_y: float = 0.0,
    ) -> None:
        super().__init__(
            id=id,
            pos=pos,
            size=self.SIZE,
            texture_name=self.TEXTURE_NAME,
            total_frames=self.TOTAL_FRAMES,
            anim_interval=self.ANIM_INTERVAL,
        )

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

        core.video.texture_blit(
            self.texture_name,
            (self.x - viewpoint.x, self.y - viewpoint.y),
            area
        )

    def animate(self) -> None:
        if pygame.time.get_ticks() - self.last_frame_change >= self.ANIM_INTERVAL:
            self.last_frame_change = pygame.time.get_ticks()
            self.curr_frame += 1
            if self.curr_frame >= self.TOTAL_FRAMES:
                self.curr_frame = 0