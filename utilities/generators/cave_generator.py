from random import randint, choice
from math import ceil
from objects import (
    Object,
    Ground,
    Obstacle,
    GroundCaves,
    CaveWalls,
    CaveBackgroundStalactites,
    CaveBones,
    Geyser,
    FallingStalactite,
)
from data_containers import objects as obj_container
from .biome_generator import BiomeGenerator

class CaveGenerator(BiomeGenerator):
    """
    Basic Cave Biome generator mainly to test/showcase the biome features.

    Attributes:
        FG_2_INTERVAL: Interval range between objects generated at FOREGROUND_2

        walls: Background walls at BACKGROUND_3
        bg_stalactites: Background stalactites at BACKGROUND_2
        last_fg2_x: Last X position of an object generated at FOREGROUND_2
    """

    FG_2_INTERVAL: tuple[int, int] = 30, 45

    OBSTACLE_RATE: dict[Obstacle.Type, int] = {
        Obstacle.Type.OIL: 15,
    }

    OBSTACLE_INTERVAL: tuple[int, int] = 10, 15

    OBSTACLES: tuple[Obstacle.Type, ...] = (
        Obstacle.Type.OIL,
    )

    OBJECT_RATE: dict[str, int] = {
        Geyser.__name__: 35,
        FallingStalactite.__name__: 15,
    }

    OBJECT_INTERVAL: dict[str, tuple[int, int]] = {
        Geyser.__name__: (20, 30),
        FallingStalactite.__name__: (15, 30),
    }

    def __init__(self, total_tiles: int) -> None:
        super().__init__(total_tiles)

        # Replacing the ground
        obj_container.delete(self.ground)
        self.ground: GroundCaves = GroundCaves(total_tiles)
        obj_container.add(self.ground)

        level_width_px: int = total_tiles * Ground.BLOCK_W

        self.walls: CaveWalls = CaveWalls(
            ceil(level_width_px / CaveWalls.BLOCK_W)
        )

        self.bg_stalactites: CaveBackgroundStalactites = CaveBackgroundStalactites(
            ceil(level_width_px / CaveBackgroundStalactites.BLOCK_W)
        )

        self.last_fg2_x: float = 0

        for obj in self.walls, self.bg_stalactites:
            obj_container.add(obj)

    def background_3(self) -> None:
        pass

    def foreground_1(self) -> None:
        pass

    def foreground_2(self) -> None:
        parallax_camera = obj_container.get_camera().rect.with_parallax(CaveBones.PARALLAX_FACTOR)

        if self.last_fg2_x + CaveBones.WIDTH >= parallax_camera.x:
            return

        if next(
            (obj for obj in obj_container.visible().values() if isinstance(obj, CaveBones)),
            None
        ) is not None:
            return

        new_pos = ceil(parallax_camera.right + CaveBones.WIDTH * 1.5), CaveBones.POS_Y
        self.last_fg2_x = new_pos[0] + randint(*self.FG_2_INTERVAL) * GroundCaves.BLOCK_W

        new_bones: CaveBones = CaveBones(new_pos)
        obj_container.queue_add(new_bones)

    def npc(self) -> None:
        pass

    def objects(self) -> None:
        end: float = self.camera.right
        draw_x: float = max(self.last_object_pos[0], self.camera.left)

        while draw_x < end:
            multiplier: int = 1

            obj_type: str = choice(tuple(self.OBJECT_RATE.keys()))

            if randint(0, 100) >= self.OBJECT_RATE[obj_type]:
                new_object = None

                if obj_type == Geyser.__name__:
                    new_object = Geyser((draw_x, 0))
                    new_object.rect.bottom = self.ground.touch_level
                elif obj_type == FallingStalactite.__name__:
                    new_object = FallingStalactite((draw_x, 0))

                obj_container.queue_add(new_object)

                self.last_object_pos = new_object.pos

                multiplier = randint(*self.OBJECT_INTERVAL[obj_type])

            draw_x += multiplier * Ground.BLOCK_W
            self.last_object_pos = draw_x, self.last_object_pos[1]