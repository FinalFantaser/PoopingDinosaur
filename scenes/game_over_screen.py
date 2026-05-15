import random
import pygame.time
from pygame import Surface
from objects import Rect
import core
from scenes.scene import Scene


class GameOverScreen(Scene):
    IMAGE_PLACEHOLDER = "game_over_placeholder.png"
    IMAGE_SIZE: tuple[float, float] = 64, 64

    BALLBUSTERS: list = [
        "ballbuster_needles",
    ]

    INPUT_INTERVAL: int = 125

    def __init__(self):
        super().__init__()

        self.picture: str = self.IMAGE_PLACEHOLDER
        self.pic_rect: Rect = Rect(0, 0, *self.IMAGE_SIZE)
        self.pic_rect.center = core.video.get_screen_rect().center
        core.video.texture_load(core.paths.TEXTURES / self.picture, self.picture)

        self.labels: dict[str, Surface] = {
            "game_over": core.gui.text_render(core.localization.translate("game_over")),
            "ballbuster": core.gui.text_render(core.localization.translate(random.choice(self.BALLBUSTERS))),
        }

        self.labels_pos: dict[str, tuple[float, float]] = {
            "game_over": (
                    self.pic_rect.center[0] - self.labels["game_over"].get_width()/2,
                    self.pic_rect.top - core.gui.MARGIN[1] - self.labels["game_over"].get_height(),
            ),

            'ballbuster': (
                    self.pic_rect.center[0] - self.labels["ballbuster"].get_width() / 2,
                    self.pic_rect.bottom + core.gui.MARGIN[1],
            )
        }

    def on_finish(self) -> None:
        core.video.texture_remove(self.picture)

    def draw_gui(self) -> None:
        for key, label in self.labels.items():
            core.video.texture_blit(label, self.labels_pos[key])

        frame: Rect = Rect(
            self.pic_rect.x - 1,
            self.pic_rect.y - 1,
            self.pic_rect.width + 2,
            self.pic_rect.height + 2,
        )
        core.video.draw_rect(frame.to_pygame_rect(), core.gui.COLOR_TEXT, 1)

        core.video.texture_blit(self.picture, self.pic_rect.pos)

    def read_input(self) -> None:
        if pygame.time.get_ticks() - core.input.last_pressed_at() < self.INPUT_INTERVAL:
            return

        if core.input.pressed("confirm") or core.input.pressed("poop") or core.input.pressed("back"):
            self.done = True
            self.next_scene = 'SelectGameMode'