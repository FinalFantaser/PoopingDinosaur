from typing import Any
import pygame.key
import pygame.time
from pygame.event import Event


ACTIONS: tuple[str, ...] = ("up", "down", "left", "right", "confirm", "back", "pause", "jump", "poop")
_bindings: dict[str, int] = {}
_events: list[Event] = []
_pressed_keys: dict[int, bool] = {}
_last_pressed: int = 0


def init(config_data: dict[str, Any]) -> None:
    global _bindings, _last_pressed
    _bindings = {
        action: pygame.key.key_code(key) for action, key in config_data.items()
    }

    _last_pressed = pygame.time.get_ticks()


def update() -> None:
    global _pressed_keys

    _events.clear()
    _events.extend(pygame.event.get())
    _pressed_keys = pygame.key.get_pressed()


def events() -> list[Event]:
    return _events.copy()


def pressed(action: str) -> bool:
    global _last_pressed
    key_code: int = _bindings[action]
    is_pressed: bool = _pressed_keys[key_code]

    if is_pressed:
        _last_pressed = pygame.time.get_ticks()

    return is_pressed


def last_pressed() -> int:
    return _last_pressed