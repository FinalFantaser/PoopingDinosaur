from math import ceil
from objects import Ground, CaveWalls, CaveBackgroundStalactites
from data_containers import objects as obj_container
from .biome_generator import BiomeGenerator


class CaveGenerator(BiomeGenerator):
    def __init__(self, total_tiles: int) -> None:
        super().__init__(total_tiles)

        level_width_px: int = total_tiles * Ground.BLOCK_W

        self.walls: CaveWalls = CaveWalls(
            ceil(level_width_px / CaveWalls.BLOCK_W)
        )

        self.bg_stalactites: CaveBackgroundStalactites = CaveBackgroundStalactites(
            ceil(level_width_px / CaveBackgroundStalactites.BLOCK_W)
        )

        for obj in self.walls, self.bg_stalactites:
            obj_container.add(obj)


    def generate(self) -> None:
        pass