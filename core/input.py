"""
Tools for reading input:
    - Keyboard
    - ... that's enough for my lazy ass
"""

from typing import Any
import pygame.key
import pygame.time
from pygame.event import Event


ACTIONS: tuple[str, ...] = ("up", "down", "left", "right", "confirm", "back", "pause", "jump", "poop")
"""List of action names to address to when checking bindings."""

_bindings: dict[str, int] = {}
"""Bindings for actions: action name -> key code."""

_events: list[Event] = []
"""list of polled pygame events."""

_events_keys: dict[str, list[Event]] = {}
"""polled pygame events filtered by type KEYDOWN or KEYUP (to avoid repeated filtering)."""

_pressed_keys: dict[int, bool] = {}
"""List if keys pressed last time the events were polled."""

_last_pressed_at: int = 0
"""Time (in ticks) when a binding was last triggered."""


def init(config_data: dict[str, Any]) -> None:
    """
    Prepare the module for work.
    :param config_data: Data from the "input" section of the config file.
    """
    global _bindings, _last_pressed_at
    _bindings = {
        action: pygame.key.key_code(key) for action, key in config_data.items()
    }

    _last_pressed_at = pygame.time.get_ticks()


def update() -> None:
    """Poll events, refresh key states."""
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
    """
    Get all polled events.

    **NOTE**: the function returns **copies** of the events, not references.

    :raises KeyError: if 'action' is not in ACTIONS.
    :return: list of events polled last time.
    """
    return _events.copy()

def pressed(action: str) -> bool:
    """
    Check if a key bound to a specific action is pressed.

    Returns ``True`` only once the button is pressed. If the key is being held down, returns ``False``.

    If ``True``, updates the `last_pressed_at` time.

    :raises KeyError: if 'action' is not in ACTIONS.
    :param action: Name of the action to check.
    :return: ``True`` if the key was just pressed.
    """

    binding: int = _bindings[action]
    return next(
        (True for event in _events_keys['down'] if event.key == binding),
        False
    )

def released(action: str) -> bool:
    """
    Check if a key bound to a specific action is released.

    Returns ``True`` only once the button was released. Afterwards, returns ``False``.

    If ``True``, updates the `last_pressed_at` time.

    :raises KeyError: if 'action' is not in ACTIONS.
    :param action: Name of the action to check.
    :return: ``True`` if the key was just released.
    """

    binding: int = _bindings[action]
    return next(
        (True for event in _events_keys['up'] if event.key == binding),
        False
    )

def held(action: str) -> bool:
    """
    Check if a key bound to a specific action is held down.

    Returns ``True`` if the key is currently pressed with no credit for whether if was pressed just now or earlier.

    If ``True``, updates the `last_pressed_at` time.

    :raises KeyError: if 'action' is not in ACTIONS.
    :param action: Name of the action to check.
    :return: ``True`` if the key is held down.
    """
    global _last_pressed_at
    key_code: int = _bindings[action]
    is_pressed: bool = _pressed_keys[key_code]

    if is_pressed:
        _last_pressed_at = pygame.time.get_ticks()

    return is_pressed


def last_pressed_at() -> int:
    """
    Get the time when a last action had been triggered, i.e. returned ``True`` when checked with
    pressed(), released() or held().

    :return: Time (ticks) when a last action had been triggered.
    """
    return _last_pressed_at