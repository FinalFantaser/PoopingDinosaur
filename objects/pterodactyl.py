import core.video
from pygame import Rect as PygameRect
from .dinosaur import Dinosaur


class Pterodactyl(Dinosaur):
    ID_STUB: str = "pterodactyl_%d"
    SIZE: tuple[float, float] = 22, 15
    TEXTURE_NAME: str = "pterodactyl.png"
    ANIM_INTERVAL: int = 250
    TOTAL_FRAMES: int = 2
    DRAW_AREA: PygameRect = PygameRect(0, 0, *SIZE)
    FOV_SIZE: tuple[float, float] = core.video.get_screen_rect().width / 2, core.video.get_screen_rect().height / 4
    VEL_X_MIN: float = 125
    VEL_X_MAX: float = VEL_X_MIN * 2.5
    VEL_X_MAX_IN: float = 1  # Seconds to reach maximum speed
    WEIGHT: float = 15.0
    WEIGHT_FACTOR: float = 0.1
    JUMP_ACCEL: float = -(WEIGHT * 8)
    HANDLER_NAME: str|None = 'PterodactylHandler'