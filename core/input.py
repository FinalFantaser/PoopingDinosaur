from typing import Any
import pygame.key
import pygame.time
from pygame.event import Event


ACTIONS: tuple[str, ...] = ("up", "down", "left", "right", "confirm", "back", "pause", "jump", "poop")
_bindings: dict[str, int] = {}
_events: list[Event] = []
_events_keys: dict[str, list[Event]] = {}
_pressed_keys: dict[int, bool] = {}
_last_pressed_at: int = 0


def init(config_data: dict[str, Any]) -> None:
    global _bindings, _last_pressed_at
    _bindings = {
        action: pygame.key.key_code(key) for action, key in config_data.items()
    }

    _last_pressed_at = pygame.time.get_ticks()


def update() -> None:
    global _pressed_keys, _events_keys

    _events.clear()
    _events.extend(pygame.event.get())
    _events_keys = {
        "up": [],
        "down": [],
    }

    for event in _events:
        if event.type == pygame.KEYDOWN:
            _events_keys["down"].append(event)
        elif event.type == pygame.KEYUP:
            _events_keys["up"].append(event)

    _pressed_keys = pygame.key.get_pressed()


def events() -> list[Event]:
    return _events.copy()

def pressed(action: str) -> bool:
    binding: int = _bindings[action]
    return next(
        (True for event in _events_keys['down'] if event.key == binding),
        False
    )

def released(action: str) -> bool:
    binding: int = _bindings[action]
    return next(
        (True for event in _events_keys['up'] if event.key == binding),
        False
    )

def held(action: str) -> bool:
    global _last_pressed_at
    key_code: int = _bindings[action]
    is_pressed: bool = _pressed_keys[key_code]

    if is_pressed:
        _last_pressed_at = pygame.time.get_ticks()

    return is_pressed


def last_pressed_at() -> int:
    return _last_pressed_at