from random import randint, choice
from math import ceil
from objects import (
    GroundHumanBase,
    HumanBaseWalls,
    HumanBaseBackground,
    HumanBaseForeground,
    Skyscraper,
)
from data_containers import objects as obj_container
from .biome_generator import BiomeGenerator

class HumanBaseGenerator(BiomeGenerator):
    BACKGROUND_2_INTERVAL: tuple[int, int] = 3, 6
    FOREGROUND_2_INTERVAL: tuple[int, int] = 5, 10
    BACKGROUND_3_RATE: int = 75
    FOREGROUND_2_RATE: int = 33

    OBJECT_RATE: dict[
        type[Skyscraper],
        int
    ] = {
        Skyscraper: 25,
        # ...
    }

    OBJECT_INTERVAL: dict[
        type[Skyscraper],
        tuple[int, int]
    ] = {
        Skyscraper: (25, 40)
    }

    OBJECTS: tuple[type[Skyscraper], ...] = tuple(OBJECT_RATE.keys())

    def __init__(self, total_tiles: int) -> None:
        super().__init__(total_tiles)

        obj_container.delete(self.ground)
        self.ground = GroundHumanBase(total_tiles)
        obj_container.add(self.ground)

        level_width_px = total_tiles * GroundHumanBase.BLOCK_W

        self.walls: HumanBaseWalls = HumanBaseWalls(
            ceil(level_width_px / HumanBaseWalls.BLOCK_W)
        )

        obj_container.add(self.walls)

    def background_2(self):
        interval = randint(*self.BACKGROUND_2_INTERVAL) * HumanBaseBackground.WIDTH
        camera = self.camera.get_copy_with_parallax(HumanBaseBackground.PARALLAX_FACTOR)

        create = camera.right - self.last_bg2_pos[0] >= interval and randint(0, 100) <= self.BACKGROUND_2_RATE

        if not create:
            return

        new_decoration = HumanBaseBackground((
            camera.right + 1,
            HumanBaseBackground.Y_POS
        ))

        self.last_bg2_pos = new_decoration.pos

        obj_container.queue_add(new_decoration)

    def background_3(self):
        pass

    def foreground_2(self):
        interval = randint(*self.FOREGROUND_2_INTERVAL) * HumanBaseForeground.WIDTH
        camera = self.camera.get_copy_with_parallax(HumanBaseForeground.PARALLAX_FACTOR)

        create = camera.right - self.last_fg2_pos[0] >= interval and randint(0, 100) <= self.FOREGROUND_2_RATE

        if not create:
            return

        new_decoration = HumanBaseForeground((
            camera.right + 1,
            HumanBaseForeground.Y_POS
        ))

        self.last_fg2_pos = new_decoration.pos

        obj_container.queue_add(new_decoration)

    def objects(self):
        obj_class: type[Skyscraper] = choice(self.OBJECTS)
        interval = randint(*self.OBJECT_INTERVAL[obj_class]) * obj_class.WIDTH
        rate = self.OBJECT_RATE[obj_class]
        create = self.camera.right - self.last_object_pos[0] >= interval and randint(0, 100) <= rate

        if not create:
            return

        new_object = obj_class((self.camera.right + 1, 0))
        new_object.rect.bottom = self.ground.touch_level
        self.last_object_pos = new_object.pos

        obj_container.queue_add(new_object)