from math import floor
from pygame import Rect as PygameRect
from pygame.time import get_ticks
import core.video
from . import TiledBackground
from .layer import Layer
from .direction import Direction



class HumanBaseWalls(TiledBackground):
    ID: str = 'human_base_walls'
    TEXTURE_NAME: str = 'human_base_bg3.png'
    BLOCK_VAR_RANGE: int = 4
    BLOCK_W: int = 64
    BLOCK_H: int = 143
    BLOCK_SIZE: tuple[float, float] = BLOCK_W, BLOCK_H
    TOTAL_FRAMES: int = 1
    ANIM_INTERVAL: int = 0
    POS: tuple[float, float] = 0, 0
    DRAW_AREA: PygameRect = PygameRect(0, 0, BLOCK_W, BLOCK_H)
    PARALLAX_FACTOR: float = 0.2

    