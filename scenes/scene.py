import pygame
from pygame.time import Clock
import pygame.event
from core.gui import COLOR_BG
from core import video
import core.input

class Scene:
    def __init__(self):
        self.fps: int = core.video.get_fps()
        self.clock: Clock = Clock()

        self.next_scene: str|None = None
        self.done: bool = False

    def run(self) -> str|None:
        while not self.done:
            self.process_events()
            self.read_input()
            self.update()

            video.clear(COLOR_BG)
            self.draw()
            self.draw_gui()
            video.refresh()
            self.clock.tick(self.fps)

        self.on_finish()
        return self.next_scene

    def process_events(self) -> None:
        core.input.update()

        for event in core.input.events():
            if event.type == pygame.QUIT:
                self.done = True
                break

    def update(self) -> None:
        pass

    def on_finish(self) -> None:
        pass

    def read_input(self) -> None:
        pass
    

    def draw(self) -> None:
        pass


    def draw_gui(self) -> None:
        pass