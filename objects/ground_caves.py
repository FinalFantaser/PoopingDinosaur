import core.video
from .ground import Ground


class GroundCaves(Ground):
    """Slightly modified version of the ground for the cave biome"""
    TEXTURE_NAME: str = 'ground_caves.png'
    BLOCK_H: int = 9
    POS_Y: float = core.video.get_screen_rect().height / 2 + BLOCK_H

    @property
    def touch_level(self) -> float:
        return self.y + self.height/2 + 1