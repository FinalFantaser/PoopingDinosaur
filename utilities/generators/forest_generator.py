from random import randint
from pygame.time import get_ticks

from objects import (
    Camera,

    Obstacle,
    Forest,
    Ground,

    Dinosaur,
    Velociraptor,
    Austroraptor,
    Pterodactyl,
    Triceratops,
    Allosaurus,
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
        Allosaurus: 10,
    }

    NPC_INTERVAL: tuple[int, int] = 15, 20

    NPC: tuple[type[Dinosaur], ...] = (
        Velociraptor,
        Austroraptor,
        Pterodactyl,
        Allosaurus,
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

    TRICERATOPS_INTERVAL: tuple[float, float] = 3500, 5000


    def __init__(self, total_tiles: int) -> None:
        super().__init__(total_tiles)

        self.forest: Forest = Forest(total_tiles)
        self.next_triceratops_spawn: int = get_ticks()
        obj_container.add(self.forest)

    def npc(self):
        """Creates NPCs within vicinity"""
        super().npc()
        self.triceratops()


    def triceratops(self) -> None:
        existing_triceratops: None | Triceratops = None
        query = obj_container.dinosaurs(Triceratops).values()

        for triceratops in query:
            existing_triceratops = triceratops

        curr_time = get_ticks()

        if existing_triceratops is None:
            if curr_time >= self.next_triceratops_spawn:
                camera = obj_container.get_camera()
                ground = obj_container.get_ground()

                new_triceratops = Triceratops((
                    camera.x - Triceratops.SIZE[0],
                    ground.touch_level - Triceratops.SIZE[1]
                ))

                obj_container.queue_add(new_triceratops)
        else:
            self.next_triceratops_spawn = curr_time + randint(*self.TRICERATOPS_INTERVAL)