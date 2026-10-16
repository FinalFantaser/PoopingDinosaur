from math import floor
from pygame import Rect as PygameRect
from pygame.time import get_ticks
import core.video
from .object import Object
from .layer import Layer
from .direction import Direction
from .trex_new import TRexNew


class TRexNewCave(TRexNew):
    """Same TRexNew, just with white contour for thhe cave biome"""
    HANDLER_NAME: str = "TRexNewHandler"
    SIZE_BODY: tuple[float, float] = 46, 18
    SIZE_HEAD: tuple[float, float] = 16, 15
    TEXTURE_NAME: str = "trex_new_cave.png"
    DRAW_AREA: PygameRect = PygameRect(0, 0, *SIZE_BODY)
    DRAW_AREA_HEAD: PygameRect = PygameRect(0, 34, *SIZE_HEAD)