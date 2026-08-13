from objects import (
    Camera,

    Obstacle,
    Forest,
    Ground,

    Dinosaur,
    Velociraptor,
    Austroraptor,
    Pterodactyl, Triceratops,
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
        Pterodactyl: 25,
    }

    NPC_INTERVAL: tuple[int, int] = 15, 20

    NPC: tuple[type[Dinosaur], ...] = (
        Velociraptor,
        Austroraptor,
        Pterodactyl,
        # ... More will be added as implemented
    )

    OBSTACLE_RATE: dict[Obstacle.Type, int] = {
        Obstacle.Type.TREE: 25,
        Obstacle.Type.STONE: 10,
        Obstacle.Type.THORNS: 42,
        Obstacle.Type.FERN: 15,
    }

    OBSTACLES: tuple[type[Obstacle], ...] = (
        Obstacle.Type.TREE,
        Obstacle.Type.STONE,
        Obstacle.Type.THORNS,
        Obstacle.Type.FERN,
    )


    def __init__(self, total_tiles: int) -> None:
        super().__init__(total_tiles)

        self.forest: Forest = Forest(total_tiles)
        obj_container.add(self.forest)

    def npc(self):
        """Creates NPCs within vicinity"""
        super().npc()

        # if len(obj_container.dinosaurs(Triceratops)) < 1:
        #     camera: Camera = obj_container.get_camera()
        #     ground: Ground = obj_container.get_ground()
        #
        #     new_triceratops = Triceratops((
        #         camera.x - Triceratops.SIZE[0],
        #         ground.touch_level
        #     ))
        #
        #     obj_container.queue_add(new_triceratops)