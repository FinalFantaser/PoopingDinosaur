from pygame import Rect as PygameRect
from .dinosaur import Dinosaur


class Austroraptor(Dinosaur):
    ID_STUB: str = "austroraptor_%d"
    SIZE: tuple[float, float] = 24, 8
    TEXTURE_NAME: str = "austroraptor.png"
    ANIM_INTERVAL: int = 125
    TOTAL_FRAMES: int = 2
    DRAW_AREA: PygameRect = PygameRect(0, 0, *SIZE)
    FOV_SIZE: tuple[float, float] = SIZE[0] * 20, SIZE[1] * 5
    VEL_X_MIN: float = 100.0
    VEL_X_MAX: float = VEL_X_MIN * 2
    VEL_X_MAX_IN: float = 1 # Seconds to reach maximum speed
    WEIGHT: float = 300.0
    WEIGHT_FACTOR: float = 0.5
    JUMP_ACCEL: float = -(WEIGHT * 0.6)
    HANDLER_NAME: str = "AustroraptorHandler"

    _total: int = 0
