from objects import Camera
from data_containers import objects as obj_container
from utilities import CaveGenerator
from .level_contract import LevelContract


class Caves(LevelContract):
    def __init__(self):
        obj_container.add(Camera())
        super().__init__(CaveGenerator(1000))