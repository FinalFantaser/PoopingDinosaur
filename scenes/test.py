from typing import Any
from pygame import Surface
import core
from scenes.scene import Scene
from objects import *
from data_containers import objects

class Test(Scene):
    def __init__(self):
        super().__init__()

        self.label: Surface = core.gui.text_render("Нажмите Esc, чтобы закрыть программу")

        self.camera: Camera = Camera((0, 0))
        self.ground: Ground = Ground(100)
        self.allosaurus: Allosaurus = Allosaurus(
            "allosaurus_main",
            (8, self.ground.y - 4),
        )

    def update(self) -> None:
        self.allosaurus.animate()

    def draw(self) -> None:
        self.ground.draw(self.camera.viewpoint)
        self.allosaurus.draw(self.camera.viewpoint)

    def draw_gui(self) -> Any:
        core.video.texture_blit(self.label, (0, 0))

    def read_input(self) -> None:
        if core.input.pressed('back'):
            self.done = True
        elif core.input.pressed('left'):
            if self.camera.left > 0:
                self.camera.left = max(0, self.camera.left - 4)
        elif core.input.pressed('right'):
            if self.camera.right < self.ground.width:
                self.camera.right = min(
                    self.ground.width,
                    self.camera.right + 4
                )