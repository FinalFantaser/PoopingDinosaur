from pygame import Surface
from pygame.font import Font
from core.paths import ASSETS as ASSETS_PATH

CAPTION: str = "My Invaders"

COLOR_BG: str = "0xBCBCBC"
COLOR_TEXT: str = "0x000000"
COLOR_TEXT_SELECTED: str = "0xFFFF00"

MARGIN: tuple[int, int] = 4, 4
PADDING: tuple[int, int] = 4, 4

FONT_NAME: str = "NineteenEightySeven-MzMJ.ttf"
FONT_SIZE: int = 7

font: Font|None = None


def init() -> None:
    global font
    font = Font(ASSETS_PATH / FONT_NAME, FONT_SIZE)


def text_render(text: str, color: str = COLOR_TEXT) -> Surface:
    return font.render(text, False, color)