import pygame.time
import pygame.transform
import core.video
from objects.object import Object, Layer, Rect


class Allosaurus(Object):
    __slots__ = (
        *Object.__slots__,
        'vel_y',
        'vel_x_modifier',
        '_hitbox',
        'invincibility',
        'last_blink',
        'visible',
        'health',
        'poos',
        'last_pooped_at',
    )

    ID: str = 'player'
    TOTAL_FRAMES: int = 2
    ANIM_INTERVAL: int = 250
    SIZE: tuple[float, float] = (53, 16)
    TEXTURE_NAME: str = 'allosaurus.png'
    LAYER: Layer = Layer.MAIN
    HANDLER_NAME: str = 'AllosaurusHandler'

    WEIGHT: float = 25.0
    MAX_POOS: int = 4
    POO_WEIGHT: float = WEIGHT / 10
    VEL_X_CONST: float = 150.0
    VEL_X_MODIFIER: float = VEL_X_CONST / 4
    VEL_Y_MIN: float = 40.0
    HITBOX_SIZE: tuple[float, float] = (32, SIZE[1])
    BLINK_INTERVAL: int = 100
    POOP_INTERVAL: int = 1000

    MAX_HEALTH: int = 5

    def __init__(
            self,
            pos: tuple[int|float, int|float],
            vel_x: float = 0.0,
            vel_y: float = 0.0,
    ) -> None:
        super().__init__(
            id=self.ID,
            pos=pos,
            size=self.SIZE,
            texture_name=self.TEXTURE_NAME,
            total_frames=self.TOTAL_FRAMES,
            anim_interval=self.ANIM_INTERVAL,
        )

        self.vel_x_modifier: float = 0.0
        self.vel_y: float = vel_y
        self._hitbox: Rect = Rect(self.x, self.y, self.HITBOX_SIZE[0], self.HITBOX_SIZE[1])
        self.invincibility: int = 0
        self.last_blink: int = pygame.time.get_ticks()
        self.visible: bool = True
        self.health: int = self.MAX_HEALTH
        self.poos: int = 0
        self.last_pooped_at: int = pygame.time.get_ticks()

    def draw(self, viewpoint: Rect) -> None:
        # Blinking when invincible
        if not self.visible:
            return

        area: tuple[int, int, int, int] = (
            int(self.curr_frame * self.width),
            0,
            int(self.width),
            int(self.height)
        )

        core.video.texture_blit(
            self.TEXTURE_NAME,
            (self.x - viewpoint.x, self.y - viewpoint.y),
            area
        )
        
    @property
    def total_weight(self) -> float:
        return self.WEIGHT + self.poos * self.POO_WEIGHT
        
    @property
    def vel_x_total(self) -> float:
        return self.VEL_X_CONST - self.POO_WEIGHT * self.poos + self.vel_x_modifier

    @property
    def hitbox(self) -> Rect:
        self._hitbox.center_x = self.rect.center_x
        self._hitbox.y = self.y

        return self._hitbox

    def animate(self) -> None:
        # Animation interval is affected by dinousaur's current speed
        anim_interval: int = int(self.ANIM_INTERVAL - self.vel_x_modifier * 2)    
    
        if pygame.time.get_ticks() - self.last_frame_change >= anim_interval:
            self.last_frame_change = pygame.time.get_ticks()
            self.curr_frame += 1
            if self.curr_frame >= self.TOTAL_FRAMES:
                self.curr_frame = 0