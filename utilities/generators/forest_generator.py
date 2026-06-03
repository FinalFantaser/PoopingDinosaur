from objects import (
    Obstacle,
    Forest,

    Dinosaur,
    Velociraptor,
    Austroraptor
)

from data_containers import objects as obj_container

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
        - Stone
        - Thorn
    """

    NPC_RATE: dict[type[Dinosaur], int] = {
        Velociraptor: 35,
        Austroraptor: 15,
    }

    NPC_INTERVAL: tuple[int, int] = 15, 20

    NPC: tuple[type[Dinosaur], ...] = (
        Velociraptor,
        Austroraptor,
        # ... More will be added as implemented
    )

    OBSTACLE_RATE: dict[Obstacle.Type, int] = {
        Obstacle.Type.TREE: 25,
        Obstacle.Type.STONE: 10,
        Obstacle.Type.THORNS: 42,
    }

    OBSTACLES: tuple[type[Obstacle], ...] = (
        Obstacle.Type.TREE,
        Obstacle.Type.STONE,
        Obstacle.Type.THORNS,
    )


    def __init__(self, total_tiles: int) -> None:
        super().__init__(total_tiles)

        self.forest: Forest = Forest(total_tiles)
        obj_container.add(self.forest)