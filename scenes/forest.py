from objects import Camera
from data_containers import objects as obj_container
from utilities import ForestGenerator
from .level_contract import LevelContract

class Forest(LevelContract):
    def __init__(self):
        obj_container.add(Camera())
        super().__init__(ForestGenerator(1000))
