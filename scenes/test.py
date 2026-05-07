import random
from typing import Any
from pygame import Surface
import core
from object_handlers.gui.pause_menu_handler import PauseMenuHandler
from scenes.scene import Scene
from objects import *
from data_containers import objects
from object_handlers import *

class Test(Scene):
    def __init__(self):
        super().__init__()

        objects.add(Camera((0, 0)))
        ground: Ground = Ground(1000)
        objects.add(ground)
        objects.add(Allosaurus((8, ground.y - 64)))
        objects.add(HealthMeter(0))
        objects.add(PooMeter(0))

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

    def update(self) -> None:
        if objects.get(PauseMenu.ID) is None:
            for obj in objects.with_handlers().values():
                object_handlers[obj.HANDLER_NAME].update(obj)

        objects.process_task_queue()

    def draw(self) -> None:
        for obj in objects.visible().values():
            obj.animate()
            obj.draw(viewpoint=objects.get_camera().rect)

    def read_input(self) -> None:
        pause_menu: PauseMenuHandler|None = objects.get(PauseMenu.ID)
        if pause_menu is not None:
            PauseMenuHandler.read_input(pause_menu)
        else:
            AllosaurusHandler.read_input(objects.get(Allosaurus.ID))
            if core.input.pressed("pause"):
                objects.add(PauseMenu())
