import math
import random

from pygame.time import get_ticks
from pygame import Rect as PygameRect
import core.video
from .tiled_background import TiledBackground, Object, Rect, Layer


class Forest(TiledBackground):
    __slots__ = *Object.__slots__, 'total_blocks', 'blocks'

    LAYER = Layer.BACKGROUND_2
    ID: str = 'forest'
    TEXTURE_NAME: str = 'bg_forest.png'
    BLOCK_VAR_RANGE: int = 2
    BLOCK_W: int = 64
    BLOCK_H: int = 64
    BLOCK_SIZE: tuple[float, float] = BLOCK_W, BLOCK_H
    TOTAL_FRAMES: int = 2
    ANIM_INTERVAL: int = 500
    POS: tuple[float, float] = 0, core.video.get_screen_rect().height / 2 - BLOCK_H
    DRAW_AREA: PygameRect = PygameRect(0, 0, BLOCK_W, BLOCK_H)
    PARALLAX_FACTOR: float = 0.2
    PTERODACTYL_TILE_RATE = 35

    def __init__(self, total_blocks: int) -> None:
        super().__init__(total_blocks)

        self.blocks: list[int] = [
            1 if self.PTERODACTYL_TILE_RATE >= random.randint(1, 100) else 0 for _ in range(self.total_blocks)
        ]

    def animate(self) -> None:
        if get_ticks() - self.last_frame_change >= self.ANIM_INTERVAL:
            self.curr_frame = (self.curr_frame + 1) % self.TOTAL_FRAMES
            self.last_frame_change = get_ticks()