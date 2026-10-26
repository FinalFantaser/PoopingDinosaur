from objects import Camera
from data_containers import objects as obj_container
from utilities.generators import HumanBaseGenerator
from .level_contract import LevelContract

class HumanBase(LevelContract):
    def __init__(self):
        obj_container.add(Camera())
        super().__init__(HumanBaseGenerator(1000))