from math import ceil
from objects import (
    GroundHumanBase, HumanBaseWalls,
)
from data_containers import objects as obj_container
from .biome_generator import BiomeGenerator

class HumanBaseGenerator(BiomeGenerator):
    def __init__(self, total_tiles: int) -> None:
        super().__init__(total_tiles)

        obj_container.delete(self.ground)
        self.ground = GroundHumanBase(total_tiles)
        obj_container.add(self.ground)

        level_width_px = total_tiles * GroundHumanBase.BLOCK_W

        self.walls: HumanBaseWalls = HumanBaseWalls(
            ceil(level_width_px / HumanBaseWalls.BLOCK_W)
        )

        obj_container.add(self.walls)


    def background_3(self):
        pass