import pygame.time
from pygame import Rect as PygameRect
import core.video
from .direction import Direction
from .dinosaur import Dinosaur


class Pterodactyl(Dinosaur):
    """
    Attributes:
        VEL_X_ACCEL: Horizontal acceleration per wings flap
        VEL_Y_MAX_ALLOWED: When reaching this speed, pterodactyl must flap its wings
        ANIM_INTERVAL: Minimum interval between wings flapping (microseconds)
        JUMP_ACCEL: Despite same name, it's a vertical acceleration per wings flap
    """

    ID_STUB: str = "pterodactyl_%d"
    SIZE: tuple[float, float] = 22, 15
    TEXTURE_NAME: str = "pterodactyl.png"
    ANIM_INTERVAL: int = 75 # Minimum interval between wings flapping (microseconds)
    TOTAL_FRAMES: int = 2
    DRAW_AREA: PygameRect = PygameRect(0, 0, *SIZE)
    FOV_SIZE: tuple[float, float] = core.video.get_screen_rect().width / 2, core.video.get_screen_rect().height / 4
    VEL_X_MIN: float = 125
    VEL_X_MAX: float = VEL_X_MIN * 2.5
    VEL_X_MAX_IN: float = 1  # Seconds to reach maximum speed
    VEL_X_ACCEL: float = VEL_X_MAX_IN / VEL_X_MIN
    VEL_Y_MIN: float = -50
    VEL_Y_MAX_ALLOWED: float = abs(VEL_Y_MIN)/2
    WEIGHT: float = 15.0
    WEIGHT_FACTOR: float = 0.1
    JUMP_ACCEL: float = WEIGHT * 8
    HANDLER_NAME: str|None = 'PterodactylHandler'

    def animate(self) -> None:
        # Switch back to free fall after flapped wings
        if self.curr_frame == 0 and pygame.time.get_ticks() - self.last_frame_change >= self.ANIM_INTERVAL:
            self.curr_frame = 1
            self.last_frame_change = pygame.time.get_ticks()


    def flap_wings(self) -> None:
        print('FLAP!!!!')
        """Flap one's wings to gain vertical and horizontal acceleration according to current direction."""
        if self.curr_frame == 1 and pygame.time.get_ticks() - self.last_frame_change >= self.ANIM_INTERVAL:
            print('NOW!!!')
            self.curr_frame = 0
            self.last_frame_change = pygame.time.get_ticks()
            self.vel_y = max(self.vel_y - self.JUMP_ACCEL, self.VEL_Y_MIN)

            if self.direction == Direction.LEFT:
                self.vel_x = max(self.vel_x - self.VEL_X_ACCEL, -self.VEL_X_MAX)
            elif self.direction == Direction.RIGHT:
                self.vel_x = min(self.vel_x + self.VEL_X_ACCEL, self.VEL_X_MAX)
        else:
            print('NOT YET')