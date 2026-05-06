import pygame
from pygame import Rect as PygameRect, Surface, key
import core.video
import core.gui
import core.localization
from objects.object import Layer, Rect, Object


class PauseMenu(Object):
    __slots__ = *Object.__slots__, "labels", "labels_pos", "selected"
    ID: str = "pause_menu"
    LAYER: Layer = Layer.GUI
    HANDLER_NAME: str | None = None
    CURSOR_RADIUS: float = 4
    INPUT_READ_INTERVAL: int = 250

    def __init__ (self) -> None:
        self.labels: dict[str, Surface] = {
            key: core.gui.text_render(core.localization.translate(key)) for key in (
                "menu_pause",
                "menu_resume",
                "menu_pause",
            )
        }

        widest_label: Surface = max(
            tuple(self.labels.values()),
            key=lambda label: label.get_width()
        )

        size: tuple[float, float] = (
            core.gui.PADDING[0] * 2 + widest_label.get_width(),
            sum((
                *(surf.get_height() for surf in self.labels.values()),
                core.gui.PADDING[1] * 2,
                core.gui.PADDING[1] * 2
            ))
        )

        super().__init__(id=self.ID, size=size)

        self.rect.center = core.video.get_screen_rect().center
        self.selected: int = 0

        self.labels_pos: dict[str, tuple[float, float]] = {}
        draw_y = self.rect.bottom + core.gui.PADDING[1]
        for key, label in self.labels.items():
            draw_x: float = self.rect.center_x - label.get_width() / 2
            self.labels_pos[key] = draw_x, draw_y
            draw_y += label.get_height() + core.gui.MARGIN[1]


    @property
    def value(self) -> str:
        return tuple(self.labels.keys())[self.selected]

    def next(self) -> str:
        self.selected += (self.selected + 1) % len(self.labels)
        return self.value

    def prev(self) -> str:
        self.selected -= (self.selected - 1) % len(self.labels)
        return self.value

    def draw(self, viewpoint: Rect) -> None:
        # Window
        for color, width in ((core.gui.COLOR_TEXT, 0), (core.gui.COLOR_BG, 1)):
            core.video.draw_rect(rect=self.rect.to_pygame_rect(), color=color, width=width)

        # Labels
        for key, label in self.labels.items():
            core.video.texture_blit(label, self.labels_pos[key])

        # Cursor
        key: str = self.value
        cursor_x: float = self.labels_pos[key][0] - self.CURSOR_RADIUS * 2 - core.gui.MARGIN[0]
        cursor_y: float = self.labels_pos[key][1] + self.labels[key].get_height()/2 - self.CURSOR_RADIUS/2

        core.video.draw_circle(center=(cursor_x, cursor_y), radius=self.CURSOR_RADIUS, color=core.gui.COLOR_TEXT)