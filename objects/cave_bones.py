from math import floor
from random import choice
from enum import IntEnum
import core.video
from .object import Rect, Layer, Object


class VarType(IntEnum):
    SKULL = 0
    BONE = 1


class CaveBones(Object):
    __slots__ = *Object.__slots__, "var_type",

    ID_STUB: str = 'cave_bones_%d'
    LAYER: Layer = Layer.FOREGROUND_2
    HANDLER_NAME: str = 'CaveBonesHandler'
    WIDTH: float = 32
    HEIGHT: float = 20
    SIZE: tuple[float, float] = WIDTH, HEIGHT
    TEXTURE_NAME: str = 'caves_fg2.png'
    PARALLAX_FACTOR: float = 1.8

    _total: int = 0
    _draw_rect: Rect = Rect(0, 0, WIDTH, HEIGHT)

    def __init__(self, pos: tuple[float, float] = (0, 0), var: None|VarType = None) -> None:
        CaveBones._total += 1

        super().__init__(
            id=self.ID_STUB % CaveBones._total,
            pos=pos,
            size=self.SIZE,
            texture_name=self.TEXTURE_NAME
        )

        self.var_type: VarType = var if var is not None else choice(tuple(VarType))