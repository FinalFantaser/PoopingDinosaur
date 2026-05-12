from typing import Any
from pathlib import Path
import pygame
from pygame import Surface, Rect, Color


COLOR_KEY: str = "0xFF00FF"
NATIVE_RESOLUTION: tuple[int, int] = 426, 240
_fps: int = 30
_fullscreen: bool = False

_buffer: Surface|None = None
_screen_rect: Rect = Rect((0, 0), NATIVE_RESOLUTION)
_textures_pool: dict[str, Surface] = {}


def init(config_data: dict[str, Any]) -> None:
    pygame.display.init()

    global _fps, _fullscreen, _buffer

    _buffer = Surface(_screen_rect.size)
    _fps = config_data["fps"]
    _fullscreen = config_data["fullscreen"]

    target_res: tuple[int, int] = tuple(int(i) for i in config_data["resolution"].split("x")[:2])
    set_video_mode(target_res)


def get_video_mode() -> tuple[int, int]:
    return pygame.display.get_surface().get_size()


def set_video_mode(res: tuple[int, int]) -> None:
    modes: list[tuple[int, int]] = pygame.display.list_modes(display=0)
    matching_mode = next(
        (mode for mode in modes if mode == res),
        pygame.display.get_desktop_sizes()[0]
    )

    pygame.display.set_mode(matching_mode)

    if get_fullscreen():
        pygame.display.toggle_fullscreen()


def clear(color: str|Color) -> None:
    _buffer.fill(color)


def refresh() -> None:
    pygame.transform.scale(
        _buffer,
        pygame.display.get_surface().get_size(),
        pygame.display.get_surface()
    )

    pygame.display.flip()


def get_fps() -> int:
    return _fps


def set_fps(new_fps: int) -> None:
    global _fps
    _fps = new_fps


def get_fullscreen() -> bool:
    return _fullscreen


def set_fullscreen(new_fullscreen: bool) -> None:
    global _fullscreen
    _fullscreen = new_fullscreen


def get_screen_rect() -> Rect:
    return _screen_rect


def textures_clear() -> None:
    _textures_pool.clear()


def texture_has(key: str) -> bool:
    return key in _textures_pool


def texture_add(key: str, surface: Surface, unique: bool = False) -> Surface:
    if key in _textures_pool and unique:
        raise KeyError(f"Duplicate texture key {key}")

    _textures_pool[key] = surface
    return surface


def texture_get(key: str, raise_error: bool = False) -> Surface | None:
    if key not in _textures_pool and raise_error:
        raise KeyError(f"No texture key {key}")

    return _textures_pool.get(key, None)


def texture_load(filepath: Path, key: str, unique: bool = False) -> Surface:
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
    if key in _textures_pool:
        _textures_pool.pop(key)
    elif raise_error:
        raise KeyError(f"Attempting to delete non-existent texture: {key}")


def texture_blit(
        texture: Surface|str,
        pos: tuple[int|float, int|float],
        area: tuple[int, int, int, int]|Rect|None = None,
) -> None:
    surface: Surface = texture if isinstance(texture, Surface) else texture_get(key=texture, raise_error=True)
    _buffer.blit(surface, pos, area)

def draw_line(start: tuple[int, int], end: tuple[int, int], color: str|Color, width: int = 0) -> None:
    pygame.draw.line(surface=_buffer, color=color, start_pos=start, end_pos=end, width=width)

def draw_pixel(pos: tuple[int, int], color: str|Color) -> None:
    draw_line(start=pos, end=pos, color=color)

def draw_rect(rect: Rect, color: str|Color, width: int = 0) -> None:
    pygame.draw.rect(surface=_buffer, color=color, rect=rect, width=width)

def draw_circle(center: tuple[int|float, int|float], radius: int|float, color: str|Color,) -> None:
    pygame.draw.circle(surface=_buffer, color=color, center=center, radius=radius)

def to_dict() -> dict[str, Any]:
    resolution: tuple[int, int] = pygame.display.get_window_size()

    return {
        "resolution": f"{resolution[0]}x{resolution[1]}",
        "fps": _fps,
        "fullscreen": _fullscreen
    }
