import random
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
        ground: Ground = Ground(1000)
        objects.add(ground)
        objects.add(Allosaurus((8, ground.y - 64)))
        objects.add(GuiHealthMeter(0))
        objects.add(GuiPooMeter(0))

        objects.get_player().poos = Allosaurus.MAX_POOS

        # Distributing clouds randomly
        draw_x: float = 0.0
        for _ in range(ground.total_tiles):
            if random.randint(1, 100) >= 90:
                objects.add(Obstacle(ObstacleType.CACTUS, (draw_x, ground.touch_level - 16)))

            if random.randint(1, 100) >= 80:
                cloud_pos: tuple[float, float] = (
                    draw_x,
                    core.video.get_screen_rect().height/4 + Cloud.SIZE[1] * random.randint(-1, 1),
                )
                objects.add(Cloud(cloud_pos))
            
            draw_x += Cloud.SIZE[0]

        self.handlers: dict[str, type[ObjectHandler]] = {
            CameraHandler.__name__: CameraHandler,
            AllosaurusHandler.__name__: AllosaurusHandler,
            PooHandler.__name__: PooHandler,

            GuiHealthMeterHandler.__name__: GuiHealthMeterHandler,
            GuiPooMeterHandler.__name__: GuiPooMeterHandler,
        }

    def update(self) -> None:
        for obj in objects.with_handlers().values():
            self.handlers[obj.HANDLER_NAME].update(obj)

        objects.process_task_queue()

    def draw(self) -> None:
        for obj in objects.visible().values():
            obj.animate()
            obj.draw(viewpoint=objects.get_camera().rect)

    def draw_gui(self) -> Any:
        core.video.texture_blit(self.label, (0, 0))

    def read_input(self) -> None:
        if core.input.pressed('back'):
            self.done = True

        AllosaurusHandler.read_input(objects.get(Allosaurus.ID))
