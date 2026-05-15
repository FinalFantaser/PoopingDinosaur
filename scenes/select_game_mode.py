from pygame import Surface, Rect as PygameRect
import pygame.time
import core
from scenes.scene import Scene


class _Card:
    IMAGE_PLACEHOLDER = "game_mode_placeholder.png"
    IMAGE_SIZE: tuple[float, float] = 128, 32

    def __init__(self, title: str, description: str, image: str = IMAGE_PLACEHOLDER) -> None:
        title_tr: str = core.localization.translate(title)
        description_tr: str = core.localization.translate(description)

        self.key: str = title
        self.surf_title: Surface = core.gui.text_render(title_tr)
        self.surf_description: Surface = core.gui.text_render(description_tr)
        self.image: str = core.localization.translate(image)

        core.video.texture_load(core.paths.TEXTURES / image, image)


    def draw(self) -> None:
        center: tuple[int, int] = core.video.get_screen_rect().center

        # Mode title label
        core.video.texture_blit(
            texture=self.surf_title,
            pos=(
                center[0] - self.surf_title.get_width()/2,
                center[1] - self.IMAGE_SIZE[1]/2 - self.surf_title.get_height() - core.gui.MARGIN[1]
            )
        )

        # Mode image
        core.video.draw_rect(
            PygameRect(
                center[0] - self.IMAGE_SIZE[0] / 2 - 1,
                center[1] - self.IMAGE_SIZE[1] / 2 - 1,
                self.IMAGE_SIZE[0] + 2,
                self.IMAGE_SIZE[1] + 2
            ),
            core.gui.COLOR_TEXT,
            1
        )

        core.video.texture_blit(
            texture=self.image,
            pos=(
                center[0] - self.IMAGE_SIZE[0]/2,
                center[1] - self.IMAGE_SIZE[1]/2
            )
        )

        # Mode description label
        core.video.texture_blit(
            texture=self.surf_description,
            pos=(
                center[0] - self.surf_description.get_width()/2,
                center[1] + self.IMAGE_SIZE[1]/2 + core.gui.MARGIN[1]
            )
        )


class SelectGameMode(Scene):
    INPUT_INTERVAL: int = 250

    def __init__(self) -> None:
        super().__init__()
        self.fps = 30

        self.cards: dict[str, _Card] = {
            "Test": _Card("game_mode_test_title", "game_mode_test_description"),
            # ...
        }

        self.entries: list[str] = list(self.cards.keys())

        self.selected: int = 0

        self.labels: dict[str, Surface] = {
            "select_game_mode": core.gui.text_render(core.localization.translate("menu_select_game_mode")),
            "prev": core.gui.text_render("<"),
            "next": core.gui.text_render(">"),
            "total": self._render_total_label()
        }

        self.labels_pos: dict[str, tuple[float, float]] = {
            "select_game_mode": (
                core.video.get_screen_rect().center[0] - self.labels["select_game_mode"].get_width()/2,
                core.gui.PADDING[1]
            ),

            "prev": (
                core.gui.PADDING[0],
                core.video.get_screen_rect().center[1] - self.labels["prev"].get_height()/2,
            ),

            "next": (
                core.video.get_screen_rect().right - self.labels["next"].get_width() - core.gui.PADDING[0],
                core.video.get_screen_rect().center[1] - self.labels["prev"].get_height() / 2,
            ),

            "total": (0, 0)
        }
        self._refresh_total_label_pos()

    def draw_gui(self) -> None:
        for key, label in self.labels_pos.items():
            core.video.texture_blit(self.labels[key], self.labels_pos[key])

        self.cards[ self.entries[self.selected] ].draw()

    def read_input(self) -> None:
        if pygame.time.get_ticks() - core.input.last_pressed_at() >= self.INPUT_INTERVAL:
            if core.input.held("left"):
                self.selected = (self.selected - 1) % len(self.entries)
                self.labels["total"] = self._render_total_label()
                self._refresh_total_label_pos()
            elif core.input.held("right"):
                self.selected = (self.selected + 1) % len(self.entries)
                self.labels["total"] = self._render_total_label()
                self._refresh_total_label_pos()

        if core.input.pressed("back"):
            self.done = True
            self.next_scene = 'MainMenu'
        if core.input.pressed("confirm") or core.input.pressed("poop"):
            self.done = True
            self.next_scene = self.entries[self.selected]


    def _render_total_label(self) -> Surface:
        return core.gui.text_render(
            f"{self.selected + 1}/{len(self.entries)}"
        )

    def _refresh_total_label_pos(self) -> None:
        self.labels_pos["total"] = (
            core.video.get_screen_rect().center[0] - self.labels["total"].get_width() / 2,
            core.video.get_screen_rect().bottom - self.labels["total"].get_height()  - core.gui.PADDING[1]
        )