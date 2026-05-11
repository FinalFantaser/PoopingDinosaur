from pygame import Surface
import core
from objects import Rect
from scenes.scene import Scene


class MainMenu(Scene):
    _INPUT_READ_INTERVAL: int = 125
    _CURSOR_RADIUS: float = 2

    def __init__(self):
        super().__init__()

        self.labels: dict[str, Surface] = {
            key: core.gui.text_render(core.localization.translate(key)) for key in (
                "menu_start",
                "menu_quit",
            )
        }

        self.labels_pos: dict[str, tuple[float, float]] = {}

        menu_rect: Rect = Rect(
            0,
            0,
            max(label.get_width() for label in self.labels.values()),
            sum(label.get_height() for label in self.labels.values()) + core.gui.MARGIN[1] * (len(self.labels) / 2),
        )

        menu_rect.center = core.video.get_screen_rect().center

        draw_y: float = menu_rect.y
        for key, label in self.labels.items():
            self.labels_pos[key] = menu_rect.center_x - label.get_width()/2, draw_y
            draw_y += label.get_height() + core.gui.MARGIN[1]

        self.menu_entries: tuple[str, ...] = "menu_start", "menu_quit"
        self.selected: int = 0

    def draw(self) -> None:
        core.video.clear(core.gui.COLOR_BG)
        for key, label in self.labels.items():
            core.video.texture_blit(label, self.labels_pos[key])

        key: str = self.menu_entries[self.selected]

        core.video.draw_circle(
            (
                self.labels_pos[key][0] - self._CURSOR_RADIUS * 2 - core.gui.MARGIN[0],
                self.labels_pos[key][1] + self.labels[key].get_height()/2 - self._CURSOR_RADIUS,
            ),
            self._CURSOR_RADIUS,
            core.gui.COLOR_TEXT
        )