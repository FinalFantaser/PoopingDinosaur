from objects import Camera, TRexNewCave
from data_containers import objects as obj_container
from utilities import CaveGenerator
from .level_contract import LevelContract


class Caves(LevelContract):
    BG_COLOR: str = "0x7c7c7c"

    def __init__(self):
        obj_container.add(Camera())
        super().__init__(CaveGenerator(1000))

        # Swapping old TRexNew with TRexNewCave
        trex_new_cave = TRexNewCave(self.trex_new.pos)
        obj_container.delete(self.trex_new)
        obj_container.add(trex_new_cave)