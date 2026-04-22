from typing import Any
from pygame import Surface, Rect
import core
from scenes.scene import Scene


class Test(Scene):
    def __init__(self):
        print('SCENE TEST')
        super().__init__()

        self.label: Surface = core.gui.text_render("Нажмите Esc, чтобы закрыть программу")
        self.rect: Rect = Rect((0, 0), core.video.get_screen_rect().size)
        self.rect.centerx, self.rect.centery = core.video.get_screen_rect().center

        print(self.rect.x, self.rect.y)

    def draw_gui(self) -> Any:
        core.video.texture_blit(self.label, (self.rect.x, self.rect.y))

    def read_input(self) -> None:
        if core.input.pressed('back'):
            self.done = True