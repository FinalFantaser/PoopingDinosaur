from random import randint
from math import ceil
from objects import Ground, GroundCaves, CaveWalls, CaveBackgroundStalactites, CaveBones
from data_containers import objects as obj_container
from .biome_generator import BiomeGenerator

class CaveGenerator(BiomeGenerator):
    FG_2_INTERVAL: tuple[int, int] = 30, 45

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

    def obstacles(self) -> None:
        pass

    def npc(self) -> None:
        pass