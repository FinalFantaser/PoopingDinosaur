from math import floor
import core.video
from .object import Rect, Object


class Geyser(Object):
    __slots__ = *Object.__slots__, 'erupting'

    HANDLER_NAME: str = 'GeyserHandler'
    ID_STUB: str = 'geyser_%d'
    WIDTH: float = 16
    HEIGHT: float = 16
    SIZE: tuple[float, float] = WIDTH, HEIGHT
    TEXTURE_NAME: str = 'geyser.png'
    TOTAL_FRAMES: int = 2
    ANIM_INTERVAL: int = 250

    _total: int = 0
    _draw_rect: Rect = Rect(0, 0, WIDTH, HEIGHT)

    def __init__(self, pos: tuple[float, float] = (0, 0)):
        Geyser._total += 1

        super().__init__(
            id=self.ID_STUB % self._total,
            pos=pos,
            size=self.SIZE,
            texture_name=self.TEXTURE_NAME,
            total_frames=self.TOTAL_FRAMES,
            anim_interval=self.ANIM_INTERVAL
        )

        self.erupting: bool = False

    def draw(self, viewpoint: Rect) -> None:
        self._draw_rect.x = self.curr_frame * self.WIDTH
        self._draw_rect.y = int(self.erupting) * self.HEIGHT

        core.video.texture_blit(
            self.TEXTURE_NAME,
            (
                floor(self.x - viewpoint.x),
                floor(self.y - viewpoint.y)
            ),
            self._draw_rect
        )