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
        MAX_ALTITUDE: Maximum altitude a pterodactyl can gain
        MAX_ROAM_DISTANCE: Range for free roaming in idle state

        last_turn_pos: X position where pterodactyl changed direction during free roaming
        gear: Metaphoric name for a wing flap interval multiplier (faster or slower)
        altitude_limit: if None, pterodactyl will fly above top of the screen
    """

    __slots__ = *Dinosaur.__slots__, 'last_turn_pos', 'gear', 'altitude_limit'

    ID_STUB: str = "pterodactyl_%d"
    SIZE: tuple[float, float] = 22, 15
    TEXTURE_NAME: str = "pterodactyl.png"
    ANIM_INTERVAL: int = 90 # Minimum interval between wings flapping (microseconds)
    TOTAL_FRAMES: int = 2
    DRAW_AREA: PygameRect = PygameRect(0, 0, *SIZE)
    FOV_SIZE: tuple[float, float] = core.video.get_screen_rect().width / 2, SIZE[1] * 3
    VEL_X_MIN: float = 125
    VEL_X_MAX: float = VEL_X_MIN * 3
    VEL_X_MAX_IN: float = 0.5  # Seconds to reach maximum speed
    VEL_X_ACCEL: float = VEL_X_MAX / VEL_X_MAX_IN
    VEL_Y_MIN: float = -50
    VEL_Y_MAX_ALLOWED: float = abs(VEL_Y_MIN)/2
    WEIGHT: float = 15.0
    WEIGHT_FACTOR: float = 0.3
    JUMP_ACCEL: float = WEIGHT * 8
    MAX_ALTITUDE: float = core.video.get_screen_rect().height / 4
    MAX_ROAM_DISTANCE: float = SIZE[0] * 3
    HANDLER_NAME: str|None = 'PterodactylHandler'

    def __init__(self, pos: tuple[int|float, int|float]):
        super().__init__(pos)
        self.last_turn_pos: float = self.rect.center_x
        self.gear: float = 1
        self.altitude_limit: float|None = self.MAX_ALTITUDE

    def animate(self) -> None:
        # Switch back to free fall after flapped wings
        if self.curr_frame == 1 and pygame.time.get_ticks() - self.last_frame_change >= self.ANIM_INTERVAL:
            self.curr_frame = 0
            self.last_frame_change = pygame.time.get_ticks()

    def flap_wings(self) -> None:
        """Flap one's wings to gain vertical and horizontal acceleration according to current direction."""
        if self.curr_frame == 0 and pygame.time.get_ticks() - self.last_frame_change >= self.ANIM_INTERVAL:
            self.curr_frame = 1
            self.last_frame_change = pygame.time.get_ticks()
            self.vel_y = max(self.vel_y - self.JUMP_ACCEL, self.VEL_Y_MIN)

            accel_x: float = self.VEL_X_ACCEL/1000 * self.update_delta * self.gear

            if self.direction == Direction.LEFT:
                self.vel_x = max(self.vel_x - accel_x, -self.VEL_X_MAX)
            elif self.direction == Direction.RIGHT:
                self.vel_x = min(self.vel_x + accel_x, self.VEL_X_MAX)
