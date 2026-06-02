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
    Austroraptor
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
    OBSTACLE_INTERVAL: tuple[int, int] = 15, 20
    OBSTACLES: tuple[Obstacle.Type, ...] = ()

    def __init__(self, total_tiles: int) -> None:
        self.camera: Camera = obj_container.get_camera()
        self.ground: Ground = Ground(total_tiles)
        obj_container.add(self.ground)

        self.last_cloud_pos: tuple[float, float] = self.camera.x - Cloud.SIZE[0], self.SKY_CENTER_LINE
        self.last_obstacle_pos: tuple[float, float] = 0, self.ground.touch_level
        self.last_npc_pos: tuple[float, float] = 0, self.ground.touch_level

    def generate(self) -> None:
        """Wrapper calling generating methods for all layers, obstacles and NPCs."""
        self.background_3()
        self.obstacles()
        # self.npc()

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
        if not self._area_big_enough(self.last_obstacle_pos[0], self.OBSTACLE_INTERVAL[0]):
            return

        area: Rect = self._make_area(self.last_obstacle_pos[0])

        if area.left - self.last_obstacle_pos[0] >= self.OBSTACLE_INTERVAL[1] * Ground.BLOCK_W:
            self.last_obstacle_pos = area.left, self.last_obstacle_pos[1]

        draw_x: float = self.last_obstacle_pos[0]

        while draw_x < area.right:
            interval_multiplier: int = 1

            ob_type: Obstacle.Type = random.choice(self.OBSTACLES)
            if self.OBSTACLE_RATE[ob_type] <= random.randint(1, 100):
                new_obstacle: Obstacle = Obstacle(ob_type, (draw_x, 0))
                new_obstacle.rect.bottom = self.ground.touch_level
                obj_container.queue_add(new_obstacle)
                self.last_obstacle_pos = new_obstacle.pos
                interval_multiplier = random.randint(*self.OBSTACLE_INTERVAL)

            draw_x += Ground.BLOCK_W * interval_multiplier

    def npc(self):
        """Creates NPCs within vicinity"""
        if not self._area_big_enough(self.last_npc_pos[0], self.NPC_INTERVAL[0]):
            return

        area: Rect = self._make_area(self.last_npc_pos[0])
        draw_x: float = self.last_npc_pos[0]
        obstacles_cache: filter = filter(
            lambda obj: isinstance(obj, Obstacle) and obj.rect.overlaps(area),
            obj_container.visible().values(),
        )

        while draw_x < area.right:
            interval_multiplier: int = 1
            npc_class: type[Dinosaur] = random.choice(self.NPC)
            tile_rect: Rect = Rect(
                draw_x,
                self.ground.touch_level - npc_class.SIZE[1],
                Ground.BLOCK_W, npc_class.SIZE[1]
            )

            if self.NPC_RATE[npc_class] <= random.randint(1, 100):
                for obs in obstacles_cache:
                    if obs.rect.overlaps(tile_rect):
                        break
                else:
                    new_npc: Dinosaur = npc_class((draw_x, 0))
                    new_npc.rect.bottom = self.ground.touch_level
                    obj_container.queue_add(new_npc)
                    self.last_npc_pos = new_npc.pos
                    interval_multiplier = random.randint(*self.NPC_INTERVAL)

            draw_x += Ground.BLOCK_W * interval_multiplier



    def _area_big_enough(self, start_point: float, min_interval: int) -> bool:
        """
        Check if an area after last object is large enough to start another generation.
        :param start_point: Left edge of the area.
        :param min_interval: Minimum interval between the generated objects.
        :return: ``True`` if area is sufficient, ``False`` otherwise.
        """
        return self.camera.right - start_point >= min_interval * Ground.BLOCK_W

    def _make_area(self, start_point: float) -> Rect:
        """
        Make an area to generate objects within.

        Positioned at: start_point : 0.

        Size (self.camera.right - start_point) x camera viewpoint height.

        :param start_point: Left edge of the area.
        """
        return Rect(start_point, 0, self.camera.right - start_point, self.camera.height)