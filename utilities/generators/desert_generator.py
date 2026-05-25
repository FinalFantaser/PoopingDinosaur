import core.video
from objects import Camera, ObstacleType, Obstacle, Austroraptor
from .biome_generator import BiomeGenerator


class DesertGenerator(BiomeGenerator):
    """
    A specific generator for desert biomes.

    Obstacles:
        - Cacti
        - Rocks
        - Tumbleweed
        - Tornadoes

    Dinosaurs:
        - Austroraptors

    """

    DINOSAURS: tuple[type[Austroraptor], ...] = Austroraptor
    OBSTACLES: tuple[ObstacleType, ... ] = ObstacleType.CACTUS
