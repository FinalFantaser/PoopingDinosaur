from objects import (
    GroundHumanBase,
)
from data_containers import objects as obj_container
from .biome_generator import BiomeGenerator

class HumanBaseGenerator(BiomeGenerator):
    def __init__(self, total_tiles: int) -> None:
        super().__init__(total_tiles)

        obj_container.delete(self.ground)
        self.ground = GroundHumanBase(total_tiles)
        obj_container.add(self.ground)


    def background_3(self):
        pass