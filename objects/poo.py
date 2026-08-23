import pygame.time
from pygame import Rect as PygameRect
import core.video
from objects.object import Rect, Object


class Poo(Object):
    __slots__ = *Object.__slots__, "vel_y", "weight", "weight_factor",
    HANDLER_NAME: str|None = "PooHandler"
    ID_STUB: str = "poo_%d"
    TEXTURE_NAME: str = "poo.png"
    SIZE: tuple[float, float] = 16, 16
    TOTAL_FRAMES: int = 2
    ANIM_INTERVAL: int = 500

    draw_rect: PygameRect = pygame.Rect((0, 0), SIZE)
    total: int = 0

    def __init__(self, pos: tuple[float, float], weight: float):
        Poo.total += 1

        super().__init__(
            id=self.ID_STUB % self.total,
            pos=pos,
            size=self.SIZE,
            texture_name=self.TEXTURE_NAME,
            total_frames=self.TOTAL_FRAMES,
            anim_interval=self.ANIM_INTERVAL
        )

        self.vel_y: float = 0.0
        self.weight: float = weight
        self.weight_factor: float = max(0.8, min(1.0, self.weight / 100))

    def animate(self):
        if pygame.time.get_ticks() - self.last_frame_change >= self.ANIM_INTERVAL:
            self.last_frame_change = pygame.time.get_ticks()
            self.curr_frame = (self.curr_frame + 1) % self.TOTAL_FRAMES

    def draw(self, viewpoint: Rect) -> None:
        draw_pos: tuple[float, float] = self.x - viewpoint.x, self.y - viewpoint.y
        self.draw_rect.x = int(self.curr_frame * self.SIZE[0])

        core.video.texture_blit(self.TEXTURE_NAME, draw_pos, self.draw_rect)