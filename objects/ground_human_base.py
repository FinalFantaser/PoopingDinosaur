from math import floor
from pygame import Rect as PygameRect
from pygame.time import get_ticks
import core.video
from .object import Object
from .layer import Layer
from .direction import Direction
from .ground import Ground


class GroundHumanBase(Ground):
    TEXTURE_NAME: str = 'ground_human_base.png'