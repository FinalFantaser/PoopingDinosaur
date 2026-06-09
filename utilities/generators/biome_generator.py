import random
import core.video
from objects import (
    Rect,
    Camera,
    Ground,
    Cloud,
    Obstacle,
    Dinosaur,
    Velociraptor,
    Austroraptor, Pterodactyl, Direction
)


from data_containers import objects as obj_container


class BiomeGenerator:
    """
    Basic generator for biomes allowing placing objects, NPCs and decorations.
    These generators are mainly intended to facilitate generation of repeating patterns.

    Attributes:
        CLOUD_INTERVAL: Interval between clouds.
        SKY_CENTER_LINE: Vertical center of the skybox.
        CLOUD_RATE: Determines how frequently clouds are placed.
        NPC_RATE: Determines how frequently NPCs are placed depending on their type.
        NPC_INTERVAL: Determines how frequently NPCs are placed.
        NPC: set of NPCs to be randomly picked from.
        OBSTACLE_RATE: Determines how frequently obstacles are placed depending on their type.
        OBSTACLE_INTERVAL: Determines how frequently NPCs are placed.
        OBSTACLES: set of obstacles to be randomly picked from.

        camera: Game camera. Obtained via data_containers.objects.get_camera()
        ground: Ground. Obtained via data_containers.objects.get_ground()
        last_cloud_pos: Position of the last cloud placed.
        last_npc_pos: Position of the last NPC placed.
        last_obstacle_pos: Position of the last obstacle placed.

    Args:
        total_tiles: Size of the generated biome in ground tiles.
    """

    CLOUD_INTERVAL: tuple[int, int] = 2, 4
    SKY_CENTER_LINE: float = core.video.get_screen_rect().height/4
    CLOUD_RATE: int = 85

    NPC_RATE: dict[type[Dinosaur], int] = {}
    NPC_INTERVAL: tuple[int, int] = 8, 10
    NPC: tuple[type[Dinosaur], ... ] = ()
    OBSTACLE_RATE: dict[Obstacle.Type, int] = {}
    OBSTACLE_INTERVAL: tuple[int, int] = 10, 15
    OBSTACLES: tuple[Obstacle.Type, ...] = ()

    def __init__(self, total_tiles: int) -> None:
        self.camera: Camera = obj_container.get_camera()
        self.ground: Ground = Ground(total_tiles)
        obj_container.add(self.ground)

        self.last_cloud_pos: tuple[float, float] = self.camera.x - Cloud.SIZE[0], self.SKY_CENTER_LINE
        self.last_obstacle_pos: tuple[float, float] = 0, 0
        self.last_npc_pos: tuple[float, float] = 0, 0

    def generate(self) -> None:
        """Wrapper calling generating methods for all layers, obstacles and NPCs."""
        self.background_3()
        self.obstacles()
        self.npc()

    def clouds(self) -> None:
        """Generate clouds in the sky as the camera moves along."""
        edge: float = self.camera.right + Cloud.SIZE[0]
        draw_x: float = max(self.last_cloud_pos[0], self.camera.left - Cloud.SIZE[0])

        while draw_x < edge:
            if draw_x - self.last_cloud_pos[0] >= random.randint(*self.CLOUD_INTERVAL) * Cloud.SIZE[0]:
                if random.randint(0, 100) >= self.CLOUD_RATE:
                    new_cloud: Cloud = Cloud((
                        draw_x,
                        self.SKY_CENTER_LINE + Cloud.SIZE[1] * random.choice([-1, 1])
                    ))

                    obj_container.queue_add(new_cloud)

                    self.last_cloud_pos = new_cloud.pos
            draw_x += Cloud.SIZE[0]


    def background_3(self):
        """Creates objects at the BACKGROUND_3 layer"""
        self.clouds()

    def obstacles(self):
        """Creates obstacles within vicinity"""
        end: float = self.camera.right
        draw_x: float = max(self.last_obstacle_pos[0], self.camera.left)

        while draw_x < end:
            multiplier: int = 1

            ob_type: Obstacle.Type = random.choice(self.OBSTACLES)

            if random.randint(0, 100) >= self.OBSTACLE_RATE[ob_type]:
                new_obstacle: Obstacle = Obstacle(
                    ob_type,
                    (draw_x, 0)
                )
                new_obstacle.rect.bottom = self.ground.touch_level

                obj_container.queue_add(new_obstacle)

                self.last_obstacle_pos = new_obstacle.pos

                multiplier = random.randint(*self.OBSTACLE_INTERVAL)

            draw_x += multiplier * Ground.BLOCK_W
            self.last_obstacle_pos = draw_x, self.last_obstacle_pos[1]


    def npc(self):
        """Creates NPCs within vicinity"""
        end: float = self.camera.right
        draw_x: float = max(self.last_npc_pos[0], self.camera.left)

        while draw_x < end:
            multiplier: int = 1

            npc_class: type[Dinosaur] = random.choice(self.NPC)

            if random.randint(0, 100) >= self.NPC_RATE[npc_class]:
                new_npc: Dinosaur = npc_class((draw_x, 0))

                if isinstance(new_npc, Pterodactyl):
                    new_npc.rect.center_y = self.SKY_CENTER_LINE + random.randint(int(-new_npc.height), int(new_npc.height))
                    new_npc.direction = random.choice((Direction.LEFT, Direction.RIGHT))
                else:
                    new_npc.rect.bottom = self.ground.touch_level

                obj_container.queue_add(new_npc)

                self.last_npc_pos = new_npc.pos

                multiplier = random.randint(*self.NPC_INTERVAL)

            draw_x += multiplier * Ground.BLOCK_W
            self.last_npc_pos = draw_x, self.last_npc_pos[1]