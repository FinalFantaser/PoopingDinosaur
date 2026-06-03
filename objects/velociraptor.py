import random
from pygame import Rect as PygameRect
import core.video
from .dinosaur import Dinosaur, Rect


class Velociraptor(Dinosaur):
    ID_STUB: str = "velociraptor_%d"
    SIZE: tuple[float, float] = 8, 7
    TEXTURE_NAME: str = "velociraptor.png"
    ANIM_INTERVAL: int = 125
    TOTAL_FRAMES: int = 2
    DRAW_AREA: PygameRect = PygameRect(0, 0, *SIZE)
    FOV_SIZE: tuple[float, float] = core.video.get_screen_rect().width / 2, core.video.get_screen_rect().height / 4
    VEL_X_MIN: float = 175
    VEL_X_MAX: float = VEL_X_MIN * 2.5
    VEL_X_MAX_IN: float = 1.3  # Seconds to reach maximum speed
    WEIGHT: float = 15.0
    WEIGHT_FACTOR: float = 0.3
    JUMP_ACCEL: float = -(WEIGHT * 3)
    HANDLER_NAME: str = 'VelociraptorHandler'

    PACK_SIZE: tuple[int, int] = 1, 3
    """Size range of a velociraptor pack"""

    _total: int = 0

    @classmethod
    def calc_pack_size(cls) -> int:
        """
        Calculate random size of a velociraptor pack.
        :return: Value within the range specified by cls.PACK_SIZE.
        """
        return random.randint(*cls.PACK_SIZE)