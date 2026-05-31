import random
import objects
from objects import Camera, Ground, Obstacle, Austroraptor
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

    def npc(self) -> None:
        edge: float = self.camera.right + Austroraptor.SIZE[0]
        draw_x: float = max(self.last_npc_pos[0], self.camera.left - Austroraptor.SIZE[0])

        while draw_x < edge:
            dino_class: type[Austroraptor] = random.choice(self.DINOSAURS)

            if random.randint(1, 100) <= self.NPC_RATE[dino_class.__name__]:
                new_dinosaur = dino_class((draw_x, self.ground.touch_level - dino_class.SIZE[1]))
                obj_container.queue_add(new_dinosaur)

            draw_x += Ground.BLOCK_W * random.randint(*self.NPC_INTERVAL[dino_class.__name__])
            self.last_npc_pos = draw_x, self.ground.touch_level

    def obstacles(self) -> None:
        edge: float = self.camera.right + Ground.BLOCK_W
        draw_x: float = max(self.last_obstacle_pos[0], self.camera.left - Austroraptor.SIZE[0])

        while draw_x < edge:
            obstacle_type: Obstacle.Type = random.choice(self.OBSTACLES)

            if random.randint(1, 100) <= self.OBSTACLE_RATE[obstacle_type]:
                new_obstacle: Obstacle = Obstacle(obstacle_type, (draw_x, 0))
                new_obstacle.rect.bottom = self.ground.touch_level
                obj_container.queue_add(new_obstacle)

            draw_x += Ground.BLOCK_W * random.randint(*self.OBSTACLE_INTERVAL[obstacle_type])
            self.last_obstacle_pos = draw_x, self.ground.touch_level