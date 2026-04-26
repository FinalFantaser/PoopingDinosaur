import math
import core.video
from objects.object import Object, Rect
from random import randint

class Ground(Object):
    __slots__ = Object.__slots__ + ('tiles', 'total_tiles')

    ID: str = 'ground'
    TEXTURE_NAME: str = 'ground.png'

    TILE_OPTIONS: int = 4
    BLOCK_W: int = 16
    BLOCK_H: int = 8
    POS_Y: float  = core.video.get_screen_rect().height / 2 + BLOCK_H

    def __init__(
            self,
            total_tiles: int,
    ) -> None:
        super().__init__(
            id=self.ID,
            pos=(0, self.POS_Y),
            size=(total_tiles * self.BLOCK_W, self.BLOCK_H),
            texture_name=self.TEXTURE_NAME,
        )

        self.tiles: tuple[int, ...] = tuple(
            randint(0, self.TILE_OPTIONS - 1) for _ in range(total_tiles)
        )

        self.total_tiles: int = total_tiles

    def draw(self, viewpoint: Rect) -> None:
        if not viewpoint.overlaps(self.rect):
            return

        start_tile: int = math.floor(viewpoint.left / self.BLOCK_W)
        end_tile: int =  min(
            math.ceil(viewpoint.right / self.BLOCK_W),
            self.total_tiles
        )

        draw_x: float = 0 - viewpoint.left % self.BLOCK_W

        for _ in range(start_tile, end_tile):
            core.video.texture_blit(
                self.texture_name,
                (draw_x, self.POS_Y),
                (self.tiles[_] * self.BLOCK_W, 0, self.BLOCK_W, self.BLOCK_H),
            )

            draw_x += self.BLOCK_W
