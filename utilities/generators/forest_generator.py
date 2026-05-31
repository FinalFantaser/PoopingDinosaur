from objects import Obstacle, Dinosaur, Velociraptor, Austroraptor
from .biome_generator import BiomeGenerator


class ForestGenerator(BiomeGenerator):
    """
    Basic forest biome generator.

    Background:
        - Forest

    Dinosaurs:
        - Velociraptor
        - Austroraptor
        - Charonosaurus
        - Allosaurus
        - Pterodactyl

    Obstacles:
        - Tree
        - Rock
        - Thorn
    """

    NPC_INTERVAL: dict[type[Dinosaur], int] = {
        Velociraptor: 40,
        Austroraptor: 25,
    }


