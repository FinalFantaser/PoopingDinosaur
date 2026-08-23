import math
import random

import pygame.time
from pygame import Rect as PygameRect
import core.video
from .object import Rect, Object


class Forest(Object):
    __slots__ = *Object.__slots__, 'total_blocks', 'blocks'

    LAYER = Object.Layer.BACKGROUND_2
    ID: str = 'forest'
    TEXTURE_NAME: str = 'bg_forest.png'
    BLOCK_VAR_RANGE: int = 2
    BLOCK_W: int = 64
    BLOCK_H: int = 64
    BLOCK_SIZE: tuple[float, float] = BLOCK_W, BLOCK_H
    TOTAL_FRAMES: int = 2
    ANIM_INTERVAL: int = 500
    POS_Y: float = core.video.get_screen_rect().height/2 - BLOCK_H
    DRAW_AREA: PygameRect = pygame.Rect(0, 0, BLOCK_W, BLOCK_H)
    PARALLAX_FACTOR: float = 0.2
    PTERODACTYL_TALE_RATE = 35

    def __init__(self, total_blocks: int) -> None:
        super().__init__(
            id=self.ID,
            pos=(0, self.POS_Y),
            size=(total_blocks * self.BLOCK_W, self.BLOCK_H),
            texture_name=self.TEXTURE_NAME
        )

        self.total_blocks: int = total_blocks
        self.blocks: list[int] = [1 if self.PTERODACTYL_TALE_RATE >= random.randint(1, 100) else 0 for _ in range(self.total_blocks)]

    def draw(self, viewpoint: Rect) -> None:
        viewpoint_parallax: Rect = Rect(
            x=viewpoint.x * self.PARALLAX_FACTOR,
            y=viewpoint.y * self.PARALLAX_FACTOR,
            width=viewpoint.width,
            height=viewpoint.height
        )

        if not viewpoint.overlaps(self.rect):
            return

        start_block: int = math.floor(viewpoint_parallax.left / self.BLOCK_W)
        end_block: int = math.ceil(viewpoint_parallax.right / self.BLOCK_W)

        draw_x: float = 0 - viewpoint_parallax.left % self.BLOCK_W

        for _ in range(start_block, end_block):
            index: int = self.blocks[_]
            curr_frame = self.curr_frame if index > 0 else  0

            self.DRAW_AREA.x = self.blocks[_] * self.BLOCK_W
            self.DRAW_AREA.y = curr_frame * self.BLOCK_H

            core.video.texture_blit(
                self.TEXTURE_NAME,
                (draw_x, self.POS_Y),
                self.DRAW_AREA
            )

            draw_x += self.BLOCK_W

    def animate(self) -> None:
        if pygame.time.get_ticks() - self.last_frame_change >= self.ANIM_INTERVAL:
            self.curr_frame = (self.curr_frame + 1) % self.TOTAL_FRAMES
            self.last_frame_change = pygame.time.get_ticks()