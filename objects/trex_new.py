import core.video

from pygame import Rect as PygameRect
from pygame.time import get_ticks

from .rect import Rect
from .separate_head_dinosaur import SeparateHeadDinosaur


class TRexNew(SeparateHeadDinosaur):
    """
    INVINCIBILITY_DURATION: default duration of invincibility state (ms).
    vel_x_modifier: acceleration/slowdown for the basic velocity depending on which direction key is pressed.
    """

    __slots__ = SeparateHeadDinosaur.__slots__ + (
        'vel_x_modifier',
        'invincibility',
        'last_blink',
        'visible',
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
    ANIM_INTERVAL_HEAD: int = 250
    TOTAL_FRAMES: int = 2
    TOTAL_FRAMES_HEAD: int = 3
    VEL_X_MIN: float = 175
    VEL_X_MIN_IN: float = 1.0 # Seconds to reach minimum velocity
    VEL_X_MODIFIER_MIN = -VEL_X_MIN * 0.25
    VEL_X_MODIFIER_MAX = VEL_X_MIN * 0.5
    VEL_X_MAX: float = VEL_X_MIN + VEL_X_MODIFIER_MAX
    ACCEL_X_PER_MICROSECOND: float = (VEL_X_MAX - VEL_X_MIN) / VEL_X_MIN_IN / 1000
    ACCEL_X_MODIFIER_PER_MICROSECOND: float = VEL_X_MODIFIER_MAX / VEL_X_MIN_IN / 1000
    INVINCIBILITY_DURATION: int = 3000
    BLINK_INTERVAL: int = 100
    WEIGHT: float = 5000.0
    WEIGHT_FACTOR: float = 0.8
    JUMP_ACCEL: float = -(WEIGHT * 0.05)
    HEALTH_MAX: int = 3
    HEAD_POS: tuple[float, float] = 38, 0
    DRAW_AREA: PygameRect = PygameRect(0, 0, *SIZE_BODY)
    DRAW_AREA_HEAD: PygameRect = PygameRect(0, 16, *SIZE_HEAD)
    FOV_SIZE: tuple[float, float] = SIZE[0] + SIZE_HEAD[0] * 2, SIZE[1]
    HITBOX_FLATTEN: tuple[float, float, float, float] = 20, 0, 16, 16
    MAX_POOS: int = 4
    POO_WEIGHT: float = abs(JUMP_ACCEL) * 0.25 / MAX_POOS
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

    def calc_anim_interval(self, init_interval: int) -> int:
        speed = self.vel_x + self.vel_x_modifier
        speed_ratio = min(speed / self.VEL_X_MAX, 1.0)
        return max(50, int(init_interval * (1.0 - 0.5 * speed_ratio)))

    @property
    def hitbox_flatten(self) -> Rect:
        main_rect = self.rect

        return Rect(
            main_rect.x + self.HITBOX_FLATTEN[0],
            main_rect.y + self.HITBOX_FLATTEN[1],
            self.HITBOX_FLATTEN[2],
            self.HITBOX_FLATTEN[3],
        )
    
    def draw(self, viewpoint: Rect) -> None:
        if not self.visible:
            return
        
        super().draw(viewpoint)
