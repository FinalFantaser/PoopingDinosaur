from pygame import Rect as PygameRect
import core.video
from .tiled_background import TiledBackground, Layer


class CaveBackgroundStalactites(TiledBackground):
    LAYER = Layer.BACKGROUND_2
    ID: str = 'cave_bg_stalactites'
    TEXTURE_NAME: str = 'caves_bg2.png'
    BLOCK_VAR_RANGE: int = 4
    BLOCK_W: int = 64
    BLOCK_H: int = 64
    BLOCK_SIZE: tuple[float, float] = BLOCK_W, BLOCK_H
    TOTAL_FRAMES: int = 1
    ANIM_INTERVAL: int = 0
    POS: tuple[float, float] = 0, core.video.get_screen_rect().height / 2 - BLOCK_H * 1.5
    DRAW_AREA: PygameRect = PygameRect(0, 0, BLOCK_W, BLOCK_H)
    PARALLAX_FACTOR: float = 0.1