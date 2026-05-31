import random
import core.video
from objects import (
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
        OBSTACLE_RATE: Determines how frequently obstacles are placed depending on their type.
        OBSTACLE_INTERVAL: Determines how frequently NPCs are placed.
        NPC: set of NPCs to be randomly picked from.
        OBSTACLES: set of obstacles to be randomly picked from.

        camera: Game camera. Obtained via data_containers.objects.get_camera()
        ground: Ground. Obtained via data_containers.objects.get_ground()
        last_cloud_pos: Position of the last cloud placed.
        last_npc_pos: Position of the last NPC placed.
        last_obstacle_pos: Position of the last obstacle placed.
    """

    CLOUD_INTERVAL: tuple[int, int] = 2, 4
    SKY_CENTER_LINE: float = core.video.get_screen_rect().height/4
    CLOUD_RATE: int = 85

    NPC_RATE: dict[type[Dinosaur], tuple[int, int]] = {}
    NPC_INTERVAL: tuple[int, int] = 8, 10
    OBSTACLE_RATE: dict[type[Obstacle], tuple[int, int]] = {}
    OBSTACLE_INTERVAL: tuple[int, int] = 15, 20
    NPC: tuple[type[Dinosaur], ... ] = ()
    OBSTACLES: tuple[Obstacle.Type, ...] = ()

    def __init__(self) -> None:
        self.camera: Camera = obj_container.get_camera()
        self.ground: Ground = obj_container.get_ground()

        self.last_cloud_pos: tuple[float, float] = self.camera.x - Cloud.SIZE[0], self.SKY_CENTER_LINE
        self.last_obstacle_pos: tuple[float, float] = 0, self.ground.touch_level
        self.last_npc_pos: tuple[float, float] = 0, self.ground.touch_level

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
        pass

    def npc(self):
        """Creates NPCs within vicinity"""
        pass

    def velociraptor(self, block: int) -> None:
        """
        Place a velociraptor pack in the specified block of ground.

        If the block is not empty (taken by an obstacle, etc.), it will be skipped. If there isn't enough space
        for a raptor pack, the generated pack will be sized to the available blocks.

        If a raptor was placed, sets last_npc_pos to its position.

        :param block: Block of ground where the pack will be placed.
        """

        camera: Camera = obj_container.get_camera()
        ground: Ground = obj_container.get_ground()
        end_point: int = min(block + Velociraptor.PACK_SIZE[1], ground.total_tiles - 1)
        pack_size: int = min(end_point - block, Velociraptor.calc_pack_size())

        if pack_size < 1:
            return