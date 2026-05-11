from typing import Any
from pathlib import Path
import pygame.mixer
from pygame.mixer import Sound


_CHANNELS_NUM: int = 4
_music_vol: float = 0.0
_sound_vol: float = 0.0
_sounds: dict[str, Sound] = {}


def init(config_data: dict[str, Any]) -> None:
    global _music_vol, _sound_vol

    _music_vol = float(config_data['music'])
    _sound_vol = float(config_data['sound'])

    if _music_vol <= 0.0 and _sound_vol <= 0.0:
        return

    pygame.mixer.init(channels=_CHANNELS_NUM)
    pygame.mixer.music.set_volume(_music_vol)


def clear() -> None:
    _sounds.clear()


def sound_has(key: str) -> bool:
    if pygame.mixer.get_init() is None:
        return False

    return key in _sounds


def sound_get(key: str) -> Sound | None:
    if pygame.mixer.get_init() is None:
        return None

    sound: Sound|None = _sounds.get(key)

    return sound


def sound_load(filepath: Path, key: str, unique: bool = False) -> Sound|None:
    if pygame.mixer.get_init() is None:
        return None

    if key in _sounds:
        if unique:
            raise KeyError(f"Duplicate sound key {key}")
        else:
            return _sounds["key"]

    new_sound: Sound = Sound(filepath)
    new_sound.set_volume(_sound_vol)
    _sounds[key] = new_sound

    return new_sound


def sound_remove(key: str, raise_error: bool = False) -> None:
    if pygame.mixer.get_init() is None or _sound_vol <= 0.0:
        return

    if key in _sounds:
        _sounds.pop(key)
    elif raise_error:
        raise KeyError(f"Attempting to delete non-existent sound: {key}")


def sound_play(key: str) -> None:
    if pygame.mixer.get_init() is not None and _sound_vol > 0.0:
        _sounds[key].play()


def music_load(filepath: Path) -> None:
    if pygame.mixer.get_init() is None or _music_vol <= 0.0:
        return

    pygame.mixer.music.load(filepath)


def music_play(repeat: bool = True) -> None:
    if pygame.mixer.get_init() is None or _music_vol <= 0.0:
        return

    pygame.mixer.music.play(loops=-1 if repeat else 0)


def music_pause() -> None:
    if pygame.mixer.get_init() is None or _music_vol <= 0.0:
        return

    pygame.mixer.music.pause()


def music_resume() -> None:
    if pygame.mixer.get_init() is None or _music_vol <= 0.0:
        return

    pygame.mixer.music.unpause()


def music_stop() -> None:
    if pygame.mixer.get_init() is None or _music_vol <= 0.0:
        return

    pygame.mixer.music.stop()


def music_set_volume(volume: float) -> None:
    if pygame.mixer.get_init() is None or _music_vol <= 0.0:
        return

    pygame.mixer.music.set_volume(volume)


def music_get_volume() -> float|None:
    if pygame.mixer.get_init() is None or _music_vol <= 0.0:
        return None

    return pygame.mixer.music.get_volume()


def to_dict() -> dict[str, Any]:
    return {
        'music_volume': _music_vol,
        'sound_volume': _sound_vol,
    }