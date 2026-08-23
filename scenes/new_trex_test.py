import core.input, core.audio
from .scene import Scene
from objects import Camera, Ground, TRexNew, PauseMenu
from object_handlers import PauseMenuHandler, TRexNewHandler, object_handlers
from utilities.generators import ForestGenerator
from data_containers import objects as obj_container, game_data

class NewTrexTest(Scene):
    def __init__(self):
        super().__init__()
        obj_container.clear()

        self.camera: Camera = Camera((0, 0))
        self.ground: Ground = Ground(1000)
        self.trex_new: TRexNew = TRexNew((
            TRexNew.SIZE[0] * 0.5,
            self.ground.y - TRexNew.SIZE[1] * 1.5)
        )
        self.trex_new.poos = TRexNew.MAX_POOS

        obj_container.add(self.camera)
        obj_container.add(self.ground)
        obj_container.add(self.trex_new)
        self.generator: ForestGenerator = ForestGenerator(self.ground.total_tiles)

    def update(self) -> None:
        if game_data.quit:
            self.done = True
            self.next_scene = 'SelectGameMode'
            game_data.quit = False
            return

        if obj_container.get_player().rect.right >= self.ground.rect.right:
            self.done = True
            self.next_scene = 'WinScreen'
            return

        if obj_container.get_player().health <= 0:
            self.done = True
            self.next_scene = 'GameOverScreen'
            return

        if obj_container.get(PauseMenu.ID) is None:
            self.generator.generate()
            self.fps = core.video.get_fps()

            for obj in obj_container.with_handlers().values():
                object_handlers[obj.HANDLER_NAME].update(obj)
        else:
            self.fps = 30

        obj_container.process_task_queue()

    def read_input(self) -> None:
        pause_menu: PauseMenu | None = obj_container.get(PauseMenu.ID)
        if pause_menu is not None:
            PauseMenuHandler.read_input(pause_menu)
        else:
            TRexNewHandler.read_input(self.trex_new)
            if core.input.pressed("pause"):
                obj_container.queue_add(PauseMenu())

    def draw(self) -> None:
        for obj in obj_container.visible().values():
            obj.animate()
            obj.draw(self.camera.rect)

    def on_finish(self) -> None:
        core.audio.clear()