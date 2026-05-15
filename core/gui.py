"""Basic tools for GUI features implementation"""

from pygame import Surface
import pygame.font
from pygame.font import Font
from core.paths import ASSETS as ASSETS_PATH

COLOR_BG: str = "0xBCBCBC"
"""Default background color."""

COLOR_TEXT: str = "0x000000"
"""Default text color."""

MARGIN: tuple[int, int] = 4, 4
"""Margin between GUI elements."""

PADDING: tuple[int, int] = 4, 4
"""Padding inside boxes."""

FONT_NAME: str = "NineteenEightySeven-MzMJ.ttf"
"""Font file name."""

FONT_SIZE: int = 7
"""Font size."""

font: Font|None = None
"""Font used for text rendering."""


def init() -> None:
    """Initialize the GUI module and prepare the font for use."""
    pygame.font.init()

    global font
    font = Font(ASSETS_PATH / FONT_NAME, FONT_SIZE)


def text_render(text: str, color: str = COLOR_TEXT) -> Surface:
    """
    Render a text surface using the default font and settings.
    :param text: String to be rendered.
    :param color: Text color.
    :return: Surface with rendered text.
    """
    return font.render(text, False, color)