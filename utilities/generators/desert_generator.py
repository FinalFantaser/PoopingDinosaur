from math import ceil
from random import randint, choice
import objects
from objects import (
    Camera,
    Ground,
    Obstacle,
    Mountains,
    CaveBones,

    Austroraptor,
)
from data_containers import objects as obj_container
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

    BACKGROUND_2_INTERVAL: tuple[int, int] = 30, 45

    NPC_RATE: dict[str, int] = {
        Austroraptor.__name__: 45,
    }

    NPC_INTERVAL: dict[str, tuple[int, int]] = {
        Austroraptor.__name__: (8, 10),
    }

    OBSTACLE_RATE: dict[Obstacle.Type, int] = {
        Obstacle.Type.CACTUS: 60,
    }

    OBSTACLE_INTERVAL: dict[Obstacle.Type, tuple[int, int]] = {
        Obstacle.Type.CACTUS: (1, 10),
    }

    DINOSAURS: tuple[type[Austroraptor], ...] = (
        getattr(objects, Austroraptor.__name__),
    )

    OBSTACLES: tuple[Obstacle.Type, ... ] = Obstacle.Type.CACTUS,

    def __init__(self, total_tiles: int) -> None:
        super().__init__(total_tiles)

        self.mountains: Mountains = Mountains(ceil(total_tiles * Ground.BLOCK_W /Mountains.BLOCK_W))
        obj_container.add(self.mountains)

    def npc(self) -> None:
        edge: float = self.camera.right + Austroraptor.SIZE[0]
        draw_x: float = max(self.last_npc_pos[0], self.camera.left - Austroraptor.SIZE[0])

        while draw_x < edge:
            dino_class: type[Austroraptor] = choice(self.DINOSAURS)

            if randint(1, 100) <= self.NPC_RATE[dino_class.__name__]:
                new_dinosaur = dino_class((draw_x, self.ground.touch_level - dino_class.SIZE[1]))
                obj_container.queue_add(new_dinosaur)

            draw_x += Ground.BLOCK_W * randint(*self.NPC_INTERVAL[dino_class.__name__])
            self.last_npc_pos = draw_x, self.ground.touch_level

    def foreground_2(self) -> None:
        parallax_camera = obj_container.get_camera().rect.with_parallax(CaveBones.PARALLAX_FACTOR)

        if self.last_fg2_pos[0] + CaveBones.WIDTH >= parallax_camera.x:
            return

        if next(
                (obj for obj in obj_container.visible().values() if isinstance(obj, CaveBones)),
                None
        ) is not None:
            return

        new_pos = ceil(parallax_camera.right + CaveBones.WIDTH * 1.5), CaveBones.POS_Y
        self.last_fg2_pos = new_pos[0] + randint(*self.FOREGROUND_2_INTERVAL) * Ground.BLOCK_W, self.last_fg2_pos[1]

        new_bones: CaveBones = CaveBones(new_pos)
        obj_container.queue_add(new_bones)

    def obstacles(self) -> None:
        edge: float = self.camera.right + Ground.BLOCK_W
        draw_x: float = max(self.last_obstacle_pos[0], self.camera.left - Austroraptor.SIZE[0])

        while draw_x < edge:
            obstacle_type: Obstacle.Type = choice(self.OBSTACLES)

            if randint(1, 100) <= self.OBSTACLE_RATE[obstacle_type]:
                new_obstacle: Obstacle = Obstacle(obstacle_type, (draw_x, 0))
                new_obstacle.rect.bottom = self.ground.touch_level
                obj_container.queue_add(new_obstacle)

            draw_x += Ground.BLOCK_W * randint(*self.OBSTACLE_INTERVAL[obstacle_type])
            self.last_obstacle_pos = draw_x, self.ground.touch_level
