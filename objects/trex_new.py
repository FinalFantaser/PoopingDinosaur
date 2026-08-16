from pygame import Rect as PygameRect
from pygame.time import get_ticks

import core.video
from .separate_head_dinosaur import SeparateHeadDinosaur


class TRexNew(SeparateHeadDinosaur):
    """
    vel_x_modifier: acceleration/slowdown for the basic velocity depending on which direction key is pressed.
    """

    __slots__ = SeparateHeadDinosaur.__slots__ + (
        'vel_x_modifier',
        'invincibility',
        'last_blink',
        'visible',
        'health',
        'poos',
        'last_pooped_at',
    )

    HANDLER_NAME: str = 'TRexNewHandler'
    ID: str = "player"
    SIZE: tuple[float, float] = 53, 16
    SIZE_BODY: tuple[float, float] = 44, 16
    SIZE_HEAD: tuple[float, float] = 15, 14
    TEXTURE_NAME: str = 'trex_new.png'
    ANIM_INTERVAL: int = 250
    ANIM_INTERVAL_HEAD: int = 100
    TOTAL_FRAMES: int = 2
    TOTAL_FRAMES_HEAD: int = 3
    VEL_X_MIN: float = 175
    VEL_X_MIN_IN: float = 1.0 # Seconds to reach minimum velocity
    VEL_X_MODIFIER_MIN = -VEL_X_MIN * 0.5
    VEL_X_MODIFIER_MAX = VEL_X_MIN * 1.5
    VEL_X_MAX: float = VEL_X_MIN + VEL_X_MODIFIER_MAX
    ACCEL_X_PER_MICROSECOND: float = VEL_X_MAX - VEL_X_MIN / VEL_X_MIN_IN / 1000
    WEIGHT: float = 5000.0
    WEIGHT_FACTOR: float = 0.8
    JUMP_ACCEL: float = -(WEIGHT * 0.0625)
    HEALTH_MAX: int = 3
    HEAD_POS: tuple[float, float] = 38, 0
    DRAW_AREA: PygameRect = PygameRect(0, 0, *SIZE_BODY)
    DRAW_AREA_HEAD: PygameRect = PygameRect(0, 16, *SIZE_HEAD)
    HITBOX_BITE_SIZE: tuple[float, float] = SIZE_HEAD
    MAX_POOS: int = 4
    POO_WEIGHT: float = WEIGHT / 50
    POOP_INTERVAL: int = 1000

    def __init__(self, pos: tuple[float, float]) -> None:
        super().__init__(pos)

        self.id = self.ID
        self.state = self.State.RUNNING
        self.invincibility: int = 0
        self.last_blink: int = get_ticks()
        self.visible: bool = True
        self.poos: int = 0
        self.last_pooped_at: int = get_ticks()
        self.vel_x_modifier: float = 0

    @property
    def weight(self) -> float:
        return self.WEIGHT + self.poos * self.POO_WEIGHT

    @property
    def weight_factor(self) -> float:
        return self.weight / self.WEIGHT