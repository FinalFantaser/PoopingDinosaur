from objects import Camera, Skyscraper
from data_containers import objects as obj_container
from utilities.generators import HumanBaseGenerator
from .level_contract import LevelContract

class HumanBase(LevelContract):
    def __init__(self):
        obj_container.add(Camera())
        super().__init__(HumanBaseGenerator(1000))

        start_x = 480
        for _ in range(100):
            scrapper = Skyscraper((start_x, 0))
            scrapper.rect.bottom = self.ground.touch_level
            start_x += 480
            obj_container.add(scrapper)