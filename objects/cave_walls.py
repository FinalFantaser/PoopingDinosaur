from pygame import Rect as PygameRect
import core.video
from .tiled_background import TiledBackground, Layer


class CaveWalls(TiledBackground):
    """Cave background"""

    LAYER = Layer.BACKGROUND_3
    ID: str = 'cave_walls'
    TEXTURE_NAME: str = 'caves_bg3.png'
    BLOCK_VAR_RANGE: int = 4
    BLOCK_W: int = 64
    BLOCK_H: int = 112
    BLOCK_SIZE: tuple[float, float] = BLOCK_W, BLOCK_H
    TOTAL_FRAMES: int = 1
    ANIM_INTERVAL: int = 0
    POS: tuple[float, float] = 0, 0
    DRAW_AREA: PygameRect = PygameRect(0, 0, BLOCK_W, BLOCK_H)
    PARALLAX_FACTOR: float = 0.2
