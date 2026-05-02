import pygame.time
import pygame.transform
import core.video
from objects.object import Object, Rect


class Allosaurus(Object):
    __slots__ = Object.__slots__ + ('poos', 'vel_y', 'vel_x_modifier')

    ID: str = 'player'
    TOTAL_FRAMES: int = 2
    ANIM_INTERVAL: int = 250
    SIZE: tuple[float, float] = (53, 16)
    TEXTURE_NAME: str = 'allosaurus.png'
    LAYER: int = 0
    HANDLER_NAME: str = 'AllosaurusHandler'

    WEIGHT: float = 25.0
    MAX_POOS: int = 4
    SINGLE_POO_WEIGHT: float = WEIGHT / 10 
    VEL_X_CONST: float = 150.0
    VEL_X_MODIFIER: float = VEL_X_CONST / 4
    VEL_X_PENALTY: float = VEL_X_CONST / 4 / MAX_POOS
    VEL_Y_MIN: float = 40.0

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

        self.poos: int = 0
        self.vel_x_modifier: float = 0.0
        self.vel_y: float = vel_y

    def draw(self, viewpoint: Rect) -> None:
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
        return self.WEIGHT + self.poos * self.SINGLE_POO_WEIGHT
        
    @property
    def vel_x_total(self) -> float:
        return self.VEL_X_CONST - (self.VEL_X_PENALTY * self.poos) + self.vel_x_modifier

    def animate(self) -> None:
        # Animation interval is affected by dinousaur's current speed
        anim_interval: int = int(self.ANIM_INTERVAL - self.vel_x_modifier * 2)    
    
        if pygame.time.get_ticks() - self.last_frame_change >= anim_interval:
            self.last_frame_change = pygame.time.get_ticks()
            self.curr_frame += 1
            if self.curr_frame >= self.TOTAL_FRAMES:
                self.curr_frame = 0
