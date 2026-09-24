from random import randint
import math
from pygame.rect import Rect as PygameRect
import core.video
from .object import Object, Layer, Rect


class TiledBackground(Object):
    """A parent class for tiled background objects using parallax"""
    __slots__ = *Object.__slots__, "total_blocks", "blocks"

    LAYER = Layer.BACKGROUND_3
    ID: str = 'tiled_background_dummy.png'
    TEXTURE_NAME: str = 'tile_background_dummy.png'
    BLOCK_VAR_RANGE: int = 2
    BLOCK_W: int = 64
    BLOCK_H: int = 64
    BLOCK_SIZE: tuple[float, float] = BLOCK_W, BLOCK_H
    TOTAL_FRAMES: int = 1
    ANIM_INTERVAL: int = 0
    POS: tuple[float, float] = 0, core.video.get_screen_rect().height / 2 - BLOCK_H
    DRAW_AREA: PygameRect = PygameRect(0, 0, BLOCK_W, BLOCK_H)
    PARALLAX_FACTOR: float = 0.2

    def __init__(self, total_blocks: int) -> None:
        super().__init__(
            id=self.ID,
            pos=self.POS,
            size=(total_blocks * self.BLOCK_W, self.BLOCK_H),
            texture_name=self.TEXTURE_NAME
        )

        self.total_blocks: int = total_blocks
        self.blocks: list[int] = [randint(0, self.BLOCK_VAR_RANGE - 1) for _ in range(self.total_blocks)]

    def draw(self, viewpoint: Rect) -> None:
        viewpoint_parallax: Rect = Rect(
            x=viewpoint.x * self.PARALLAX_FACTOR,
            y=viewpoint.y * self.PARALLAX_FACTOR,
            width=viewpoint.width,
            height=viewpoint.height
        )

        if not viewpoint_parallax.overlaps(self.rect):
            return

        parallax_x = math.floor(viewpoint.x * self.PARALLAX_FACTOR)
        start_block = parallax_x // self.BLOCK_W
        end_block = math.ceil((parallax_x + viewpoint.width) / self.BLOCK_W)
        draw_x = -(parallax_x % self.BLOCK_W)

        for _ in range(start_block, end_block):
            index: int = self.blocks[_]
            curr_frame = self.curr_frame if index > 0 else  0

            self.DRAW_AREA.x = self.blocks[_] * self.BLOCK_W
            self.DRAW_AREA.y = curr_frame * self.BLOCK_H

            core.video.texture_blit(
                self.TEXTURE_NAME,
                (draw_x, self.POS[1]),
                self.DRAW_AREA
            )

            draw_x += self.BLOCK_W