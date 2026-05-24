import random
from typing import Any
from pygame import Surface
import core
from object_handlers.gui.pause_menu_handler import PauseMenuHandler
from scenes.scene import Scene
from objects import *
from data_containers import objects, game_data
from object_handlers import *
from utilities.generators import BiomeGenerator

class Test(Scene):
    def __init__(self):
        super().__init__()

        self.camera: Camera = Camera((0, 0))
        self.ground: Ground = Ground(1000)
        self.mountains: list[Mountains] = []

        objects.clear()
        objects.add(self.camera)
        objects.add(self.ground)
        objects.add(TRex((8, self.ground.y - 64)))
        objects.add(HealthMeter(0))
        objects.add(PooMeter(0))

        objects.get_player().poos = TRex.MAX_POOS

        self.generator: BiomeGenerator = BiomeGenerator(self.camera)

        # Distributing obstacles and dinosaurs
        draw_x: float = 0.0
        for _ in range(self.ground.total_tiles):
            if random.randint(1, 100) >= 90:
                objects.add(Obstacle(ObstacleType.CACTUS, (draw_x, self.ground.touch_level - 16)))
            elif random.randint(1, 100) >= 95:
                objects.add(Austroraptor((draw_x, self.ground.touch_level - Austroraptor.SIZE[1])))

            draw_x += Cloud.SIZE[0]

        # Loading sounds and music
        for idx in range(1, 3):
            key: str = f"fart_{idx}"
            core.audio.sound_load(core.paths.SOUNDS / f"{key}.wav", key)

    def update(self) -> None:
        if game_data.quit:
            self.done = True
            self.next_scene = 'SelectGameMode'
            game_data.quit = False
            return

        if objects.get_player().rect.right >= self.ground.rect.right:
            self.done = True
            self.next_scene = 'WinScreen'
            return

        if objects.get_player().health <= 0:
            self.done = True
            self.next_scene = 'GameOverScreen'
            return

        if objects.get(PauseMenu.ID) is None:
            self.generator.background_3()
            self.fps = core.video.get_fps()

            for obj in objects.with_handlers().values():
                object_handlers[obj.HANDLER_NAME].update(obj)
        else:
            self.fps = 30

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
            TRexHandler.read_input(objects.get(TRex.ID))
            if core.input.pressed("pause"):
                objects.add(PauseMenu())

    def on_finish(self) -> None:
        core.audio.clear()