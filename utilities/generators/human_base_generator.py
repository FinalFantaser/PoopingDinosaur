from random import randint, choice
from math import ceil
from pygame.time import get_ticks
from objects import (
    GroundHumanBase,
    HumanBaseWalls,
    HumanBaseBackground,
    HumanBaseForeground,
    Skyscraper,
    LandMine,
    Tesla,
    Lighting,
    MissileSilo,

    Helicopter,
    Scientist,
)
from data_containers import objects as obj_container
from .biome_generator import BiomeGenerator

class HumanBaseGenerator(BiomeGenerator):
    BACKGROUND_2_INTERVAL: tuple[int, int] = 3, 6
    FOREGROUND_2_INTERVAL: tuple[int, int] = 5, 10
    BACKGROUND_3_RATE: int = 75
    FOREGROUND_2_RATE: int = 33

    NPC_RATE: dict[
        type[Scientist],
        int
    ] = {
        Scientist: 40,
    }

    NPC_INTERVAL: dict[
        type[Scientist],
        tuple[int, int],
    ] = {
        Scientist: (15, 20),
    }

    NPC: tuple[
        type[Scientist],
        ...
    ] = tuple(NPC_RATE.keys())

    OBJECT_RATE: dict[
        type[Skyscraper|LandMine|Tesla|MissileSilo],
        int
    ] = {
        Skyscraper: 25,
        LandMine: 15,
        Tesla: 15,
        MissileSilo: 30,
    }

    OBJECT_INTERVAL: dict[
        type[Skyscraper|LandMine|Tesla|MissileSilo],
        tuple[int, int]
    ] = {
        Skyscraper: (25, 40),
        LandMine: (15, 30),
        Tesla: (10, 20),
        MissileSilo: (10, 20),
    }

    OBJECTS: tuple[
        type[Skyscraper|LandMine|Tesla|MissileSilo],
        ...
    ] = tuple(OBJECT_RATE.keys())

    HELICOPTER_SPAWN_RANGE: tuple[int, int] = 1500, 2000

    def __init__(self, total_tiles: int) -> None:
        super().__init__(total_tiles)

        self.next_helicopter_spawn: int = get_ticks() + randint(*self.HELICOPTER_SPAWN_RANGE)

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
        interval = randint(*self.OBJECT_INTERVAL[obj_class]) * self.ground.BLOCK_W
        rate = self.OBJECT_RATE[obj_class]

        if rate > 0:
            create = self.camera.right - self.last_object_pos[0] >= interval and randint(0, 100) <= rate
        else:
            create = False

        if not create:
            return

        if obj_class is Tesla:
            self.teslas()
            return

        new_object = obj_class((self.camera.right + 1, 0))
        self.put_on_ground(new_object)
        self.last_object_pos = new_object.pos
        obj_container.queue_add(new_object)

    def npc(self):
        npc_class: type[Scientist] = choice(self.NPC)
        interval = randint(*self.NPC_INTERVAL[npc_class]) * self.ground.BLOCK_W
        rate = self.NPC_RATE[npc_class]

        if rate > 0:
            create = self.camera.right - self.last_npc_pos[0] >= interval and randint(0, 100) <= rate
        else:
            create = False

        if create:
            new_npc = npc_class((self.camera.right + 1, 0))
            self.put_on_ground(new_npc)
            self.last_npc_pos = new_npc.pos
            obj_container.queue_add(new_npc)

        self.helicopters()

    def teslas(self):
        tesla_1 = Tesla((self.camera.right + 1, 0))
        self.put_on_ground(tesla_1)

        tesla_2 = Tesla((
                tesla_1.rect.right + tesla_1.gap * Lighting.WIDTH,
                tesla_1.y,
        ))

        tesla_1.connect(tesla_2)
        self.last_object_pos = tesla_2.pos

        obj_container.queue_add(tesla_1)
        obj_container.queue_add(tesla_2)

    def helicopters(self):
        existing_helicopter: None|Helicopter = None

        for obj in obj_container.main_layer().values():
            if isinstance(obj, Helicopter):
                existing_helicopter = obj
                break

        if existing_helicopter is not None:
            return

        curr_time = get_ticks()

        if curr_time < self.next_helicopter_spawn:
            return

        # Prevents spawning next helicopter immediately after the last one
        if curr_time - self.next_helicopter_spawn >= self.HELICOPTER_SPAWN_RANGE[1]:
            self.next_helicopter_spawn = curr_time + randint(*self.HELICOPTER_SPAWN_RANGE)
            return

        new_helicopter = Helicopter((
                self.camera.left - Helicopter.WIDTH,
                self.SKY_CENTER_LINE - Helicopter.HEIGHT/2,
        ))

        obj_container.add(new_helicopter)
        self.next_helicopter_spawn = curr_time + randint(*self.HELICOPTER_SPAWN_RANGE)