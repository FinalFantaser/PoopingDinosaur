from pygame import Surface
import core
from scenes.scene import Scene


class _Card:
    IMAGE_PLACEHOLDER = 'game_mode_placeholder.png'

    def __init__(self, title: str, description: str, image: str = IMAGE_PLACEHOLDER) -> None:
        title_tr: str = core.localization.translate(title)
        description_tr: str = core.localization.translate(description)

        self.key: str = title
        self.surf_title: Surface = core.gui.text_render(title_tr)
        self.surf_description: Surface = core.gui.text_render(description_tr)
        self.image: str = core.localization.translate(image)

        core.video.texture_load(core.paths.TEXTURES / image, image)

    def draw(self) -> None:
        pass

class SelectGameMode(Scene):
    pass