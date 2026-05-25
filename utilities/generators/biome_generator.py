import random
import core.video
from objects import Camera, Ground, Obstacle, Cloud
from data_containers import objects as obj_container


class BiomeGenerator:
    """
    Basic generator for biomes allowing placing objects, NPCs and decorations.
    These generators are mainly intended to facilitate generation of repeating patterns.
    """

    CLOUD_INTERVAL: tuple[int, int] = 2, 4
    SKY_CENTER_LINE: float = core.video.get_screen_rect().height/4
    CLOUD_RATE: int = 85

    def __init__(self) -> None:
        """
        :param camera: Camera to determine borders to place objects.
        """
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
