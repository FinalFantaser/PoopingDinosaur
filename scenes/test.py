from typing import Any
from pygame import Surface
import core
from scenes.scene import Scene
from objects import *
from data_containers import objects
from object_handlers import *

class Test(Scene):
    def __init__(self):
        super().__init__()

        self.label: Surface = core.gui.text_render("Нажмите Esc, чтобы закрыть программу")

        objects.add(Camera((0, 0)))
        ground: Ground = Ground(100)
        objects.add(ground)
        objects.add(Allosaurus(
            "allosaurus_main",
            (8, ground.y - 64),
        ))

        self.handlers: dict[str, type[ObjectHandler]] = {
            AllosaurusHandler.__name__: AllosaurusHandler,
        }

    def update(self) -> None:
        for obj in objects.with_handlers().values():
            self.handlers[obj.HANDLER_NAME].update(obj)

    def draw(self) -> None:
        for obj in objects.visible().values():
            obj.animate()
            obj.draw(viewpoint=objects.get_camera().rect)

    def draw_gui(self) -> Any:
        core.video.texture_blit(self.label, (0, 0))

    def read_input(self) -> None:
        if core.input.pressed('back'):
            self.done = True
    #     elif core.input.pressed('left'):
    #         if self.camera.left > 0:
    #             self.camera.left = max(0, self.camera.left - 4)
    #     elif core.input.pressed('right'):
    #         if self.camera.right < self.ground.width:
    #             self.camera.right = min(
    #                 self.ground.width,
    #                 self.camera.right + 4
    #             )