from random import randint, choice
from math import ceil
from objects import (
    GroundHumanBase,
    HumanBaseWalls,
    HumanBaseBackground,
    HumanBaseForeground,
    Skyscraper,
    LandMine,
    Tesla,
    Lighting,
)
from data_containers import objects as obj_container
from .biome_generator import BiomeGenerator

class HumanBaseGenerator(BiomeGenerator):
    BACKGROUND_2_INTERVAL: tuple[int, int] = 3, 6
    FOREGROUND_2_INTERVAL: tuple[int, int] = 5, 10
    BACKGROUND_3_RATE: int = 75
    FOREGROUND_2_RATE: int = 33

    OBJECT_RATE: dict[
        type[Skyscraper|LandMine|Tesla],
        int
    ] = {
        Skyscraper: 25,
        LandMine: 15,
        Tesla: 35
    }

    OBJECT_INTERVAL: dict[
        type[Skyscraper|LandMine|Tesla],
        tuple[int, int]
    ] = {
        Skyscraper: (25, 40),
        LandMine: (15, 30),
        Tesla: (10, 20),
    }

    OBJECTS: tuple[type[Skyscraper|LandMine], ...] = tuple(OBJECT_RATE.keys())

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
        obj_class: type[Skyscraper|LandMine|Tesla] = choice(self.OBJECTS)
        interval = randint(*self.OBJECT_INTERVAL[obj_class]) * obj_class.WIDTH
        rate = self.OBJECT_RATE[obj_class]
        create = self.camera.right - self.last_object_pos[0] >= interval and randint(0, 100) <= rate

        if not create:
            return

        if obj_class is Tesla:
            self.teslas()
            return

        new_object = obj_class((self.camera.right + 1, 0))
        self.put_on_ground(new_object)
        self.last_object_pos = new_object.pos
        obj_container.queue_add(new_object)

    def teslas(self):
        tesla_1 = Tesla((self.camera.right + 1, 0))
        self.put_on_ground(tesla_1)

        tesla_2 = Tesla((
                tesla_1.rect.right + tesla_1.gap * Lighting.WIDTH,
                tesla_1.y,
        ))

        tesla_1.couple = tesla_2.id
        self.last_object_pos = tesla_2.pos

        obj_container.queue_add(tesla_1)
        obj_container.queue_add(tesla_2)