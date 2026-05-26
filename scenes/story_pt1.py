from .scene import Scene
from objects import *


class StoryPt1(Scene):
    def __init__(self):
        super().__init__()

        self.ground: Ground = Ground(1500)
        self.camera: Camera = Camera((0, 0))
