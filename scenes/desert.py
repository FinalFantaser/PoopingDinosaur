from objects import Camera
from data_containers import objects as obj_container
from utilities.generators import DesertGenerator
from .level_contract import LevelContract


class Desert(LevelContract):
    def __init__(self):
        obj_container.add(Camera())
        super().__init__(DesertGenerator(1000))