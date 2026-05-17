"""
Tools for video:
    - Video modes handling
    - FPS handling
    - Textures handling and rendering
    - Shapes rendering
"""

from typing import Any
from pathlib import Path
import pygame
from pygame import Surface, Rect, Color


COLOR_KEY: str = "0xFF00FF"
"""Background color te be cut from sprite textures."""

NATIVE_RESOLUTION: tuple[int, int] = 426, 240
"""Native game resolution (scaled to actual resolution)."""

_fps: int = 30
"""Game frame rate."""

_fullscreen: bool = False
"""Fullscreen mode flag."""

_buffer: Surface|None = None
"""Video buffer used for actual rendering before scaling to actual resolution."""

_screen_rect: Rect = Rect((0, 0), NATIVE_RESOLUTION)
"""Pygame Rect object to facilitate positioning inside the native resolution viewpoint."""

_textures_pool: dict[str, Surface] = {}
"""Loaded textures available by key."""


def init(config_data: dict[str, Any]) -> None:
    """
    Initialize the video mode and FPS and prepare the module for work.

    :param config_data: Data from the "video" section of the config file.
    """
    pygame.display.init()

    global _fps, _fullscreen, _buffer

    _buffer = Surface(_screen_rect.size)
    _fps = config_data["fps"]
    _fullscreen = config_data["fullscreen"]

    target_res: tuple[int, int] = tuple(int(i) for i in config_data["resolution"].split("x")[:2])
    set_video_mode(target_res)


def get_video_mode() -> tuple[int, int]:
    """
    Get actual video mode.

    :return: Actual (not native) video mode used by the game.
    """
    return pygame.display.get_surface().get_size()


def set_video_mode(res: tuple[int, int]) -> None:
    """
    Set video mode.

    :param res: Screen width and height.
    """
    modes: list[tuple[int, int]] = pygame.display.list_modes(display=0)
    matching_mode = next(
        (mode for mode in modes if mode == res),
        pygame.display.get_desktop_sizes()[0]
    )

    pygame.display.set_mode(matching_mode)

    if get_fullscreen():
        pygame.display.toggle_fullscreen()


def clear(color: str|Color) -> None:
    """
    Fill the screen with specified color.

    :param color: Color to fill the screen.
    """
    _buffer.fill(color)


def refresh() -> None:
    """Refresh the screen. Inner native resolution buffer is scaled to the actual game resolution."""
    pygame.transform.scale(
        _buffer,
        pygame.display.get_surface().get_size(),
        pygame.display.get_surface()
    )

    pygame.display.flip()


def get_fps() -> int:
    """Get current FPS value."""
    return _fps


def set_fps(new_fps: int) -> None:
    """Set FPS."""
    global _fps
    _fps = new_fps


def get_fullscreen() -> bool:
    """
    Check if the game is run in fullscreen mode.

    :return: ``True`` if fullscreen, ``False`` if windowed.
    """
    return _fullscreen


def set_fullscreen(new_fullscreen: bool) -> None:
    """
    Set fullscreen mode.

    :param new_fullscreen: ``True`` for fullscreen, ``False`` for windowed mode.
    """
    global _fullscreen
    _fullscreen = new_fullscreen


def get_screen_rect() -> Rect:
    """Get screen rect."""
    return _screen_rect


def textures_clear() -> None:
    """Clear the textures pool."""
    _textures_pool.clear()


def texture_has(key: str) -> bool:
    """
    Check if the texture pool has the specified key.

    :param key: Texture key to check.
    :return: ``True`` if the pool has the key, ''False'' otherwise.
    """
    return key in _textures_pool


def texture_add(surface: Surface, key: str, unique: bool = False) -> Surface:
    """
    Add an existing surface to the texture pool.

    :param surface: texture to be added.
    :param key: key to store the texture with.
    :param unique: raise KeyError if the key already exists.
    :raises KeyError: if the key already exists and the **unique** parameter is ``True``.
    :return: Added texture.
    """
    if key in _textures_pool and unique:
        raise KeyError(f"Duplicate texture key {key}")

    _textures_pool[key] = surface
    return surface


def texture_get(key: str, raise_error: bool = False) -> Surface | None:
    """
    Get a texture from the pool by key.

    :param key: Key of the texture.
    :param raise_error: raise a KeyError if the key does not exist.
    :raises KeyError: if the key does not exist.
    :return: Surface or None if the key does not exist.
    """
    if key not in _textures_pool and raise_error:
        raise KeyError(f"No texture key {key}")

    return _textures_pool.get(key, None)


def texture_load(filepath: Path, key: str, unique: bool = False) -> Surface:
    """
    Load a texture from file to the pool under the specified key.

    If **unique** is ``False`` and such key already exists in the pool, new texture won't be loaded,
    and the one stored under the specified key will be returned.

    :param filepath: Path to the texture file.
    :param key: Key for the pool.
    :param unique: Raise KeyError if such key already exists in the pool.
    :raises KeyError: if such key already exists and **unique** is ``True``.
    :return: New or existing texture.
    """
    if key in _textures_pool:
        if unique:
            raise KeyError(f"Duplicate texture key {key}")
        else:
            return texture_get(key)

    new_surf: Surface = pygame.image.load(filepath)
    new_surf.set_colorkey(COLOR_KEY)
    _textures_pool[key] = new_surf

    return new_surf


def texture_remove(key: str, raise_error: bool = False) -> None:
    """
    Delete a texture under the specified key from the texture pool.

    :param key: texture key.
    :param raise_error: raise a KeyError if the key does not exist.
    :raises KeyError: if the key does not exist and **raise_error** is ``True``.
    """
    if key in _textures_pool:
        _textures_pool.pop(key)
    elif raise_error:
        raise KeyError(f"Attempting to delete non-existent texture: {key}")


def texture_blit(
        texture: Surface|str,
        pos: tuple[int|float, int|float],
        area: tuple[int, int, int, int]|Rect|None = None,
) -> None:
    """
    Blit a texture onto the buffer surface. Texture can be accessed by a key, or a standalone texture can be used.

    :param texture: key of the texture in the pool or a standalone texture.
    :param pos: position to blit the texture.
    :param area: area for partial blit. If none, while texture will be blitted.
    """
    surface: Surface = texture if isinstance(texture, Surface) else texture_get(key=texture, raise_error=True)
    _buffer.blit(surface, pos, area)

def draw_line(start: tuple[int, int], end: tuple[int, int], color: str|Color, width: int = 0) -> None:
    """
    Draw a line on the buffer surface.

    :param start: Starting point.
    :param end: Ending point.
    :param color: Color for the line.
    :param width: Width of the line.
    """
    pygame.draw.line(surface=_buffer, color=color, start_pos=start, end_pos=end, width=width)

def draw_pixel(pos: tuple[int, int], color: str|Color) -> None:
    """
    Draw a pixel on the buffer surface.

    :param pos: Position of the pixel.
    :param color: Color for the pixel.
    :return:
    """
    draw_line(start=pos, end=pos, color=color)

def draw_rect(rect: Rect, color: str|Color, width: int = 0) -> None:
    """
    Draw/fill a rectangle on the buffer surface.

    :param rect: pygame Rect object for size and position.
    :param color: Color for the rectangle.
    :param width: Border width. If `0`, the rectangle will be filled.
    """
    pygame.draw.rect(surface=_buffer, color=color, rect=rect, width=width)

def draw_circle(
        center: tuple[int|float, int|float],
        radius: int|float,
        color: str|Color,
        width: int = 0,
) -> None:
    """
    Draw/fill a circle on the buffer surface.

    :param center: Center of the circle.
    :param radius: Radius of the circle.
    :param color: Color for the circle.
    :param width: Border width. If `0`, the circle will be filled.
    """
    pygame.draw.circle(surface=_buffer, color=color, center=center, radius=radius, width=width)

def to_dict() -> dict[str, Any]:
    """
    Pack video configuration data into a dict (e.g. for saving into a config file).
    :return: key-value dict of video configuration data.
    """
    resolution: tuple[int, int] = pygame.display.get_window_size()

    return {
        "resolution": f"{resolution[0]}x{resolution[1]}",
        "fps": _fps,
        "fullscreen": _fullscreen
    }
