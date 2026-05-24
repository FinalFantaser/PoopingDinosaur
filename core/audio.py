"""
Tools for audio:
    - Sounds playback
    - Music playback
    - Volume adjustment
"""

from typing import Any
from pathlib import Path
import pygame.mixer
from pygame.mixer import Sound


_CHANNELS_NUM: int = 4
"""Maximum number of sounds that can be played at once."""

_music_vol: float = 0.0
"""Music volume"""

_sound_vol: float = 0.0
"""Sound volume"""

_sounds: dict[str, Sound] = {}
"""Pool of sounds keyed with and id available for playback."""


def init(config_data: dict[str, Any]) -> None:
    """
    Initialize pygame.mixer and prepare the module for work.

    **NOTE**: does not initialize pygame.mixer if music and sound volume is 0.

    :param config_data: Data from the "audio" section of the config file.
    :return:
    """

    global _music_vol, _sound_vol

    _music_vol = float(config_data['music'])
    _sound_vol = float(config_data['sound'])

    if _music_vol <= 0.0 and _sound_vol <= 0.0:
        return

    pygame.mixer.init(channels=_CHANNELS_NUM)
    pygame.mixer.music.set_volume(_music_vol)


def clear() -> None:
    """Clear the sound pool."""
    _sounds.clear()


def sound_has(key: str) -> bool:
    """
    Check if a sound with the given key is in the pool.

    **NOTE:**: Always returns ``False`` if pygame.mixer was not initialized.

    :param key: key to check.
    :return: ``True`` if the pool has the key, ''False'' otherwise.
    """
    if pygame.mixer.get_init() is None:
        return False

    return key in _sounds


def sound_get(key: str) -> Sound | None:
    """
    Get a sound by key from the pool.

    :param key: key of the sound to get
    :return: Sound object or ``None`` if not found.
    """

    sound: Sound|None = _sounds.get(key)

    return sound


def sound_load(filepath: Path, key: str, unique: bool = False) -> Sound|None:
    """
    Load sound from a file and add it to the pool under the specified key.

    If a sound with the given key already exists and 'unique' is ``False``, it will be replaced with the new sound.

    **NOTE:** Always returns ``None`` if pygame.mixer was not initialized.

    :param filepath: path to the sound file to load.
    :param key: key for the sound object to add to the pool.
    :param unique: raise KeyError if a sound with the given key already exists in the pool.
    :raises KeyError: if a sound with the given key already exists in the pool and 'unique' is ``True``.
    :return: Loaded Sound or ``None`` if pygame.mixer was not initialized.
    """
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
    """
    Delete sound from the pool by the given key.

    **NOTE:**: Does nothing if pygame.mixer was not initialized.

    :param key: key of the sound to remove.
    :param raise_error: raise KeyError if the given key is not in the pool.
    :raises KeyError: if a sound with the given key is not in the pool.
    """
    if pygame.mixer.get_init() is None or _sound_vol <= 0.0:
        return

    if key in _sounds:
        _sounds.pop(key)
    elif raise_error:
        raise KeyError(f"Attempting to delete non-existent sound: {key}")


def sound_play(key: str) -> None:
    """
    Play a sound from the pool.

    **NOTE:**: Does nothing if pygame.mixer was not initialized.
    **NOTE:**: Does nothing if sound volume is 0.

    :param key: Key of the sound object to play.
    """
    if pygame.mixer.get_init() is not None and _sound_vol > 0.0:
        _sounds[key].play()


def music_load(filepath: Path) -> None:
    """
    Load a music file into pygame.mixer.music.

    Note that despite being based on SDL2 pygame restricts music to only one file loaded at once. Should other music
    file be loaded, it replaces the previous one.

    **NOTE:**: Does nothing if pygame.mixer was not initialized.
    **NOTE:**: Does nothing if music volume is 0.

    :param filepath: path to the music file to load.
    """
    if pygame.mixer.get_init() is None or _music_vol <= 0.0:
        return

    pygame.mixer.music.load(filepath)


def music_play(repeat: bool = True) -> None:
    """
    Play a music file currently loaded into pygame.mixer.music.

    **NOTE:**: Does nothing if pygame.mixer was not initialized.
    **NOTE:**: Does nothing if music volume is 0.

    :param repeat: ``True`` to loop the music and ``False`` to stop as the track ends.
    """
    if pygame.mixer.get_init() is None or _music_vol <= 0.0:
        return

    pygame.mixer.music.play(loops=-1 if repeat else 0)


def music_pause() -> None:
    """
    Pause music is played.

    **NOTE:**: Does nothing if pygame.mixer was not initialized.
    **NOTE:**: Does nothing if music volume is 0.
    """
    if pygame.mixer.get_init() is None or _music_vol <= 0.0:
        return

    pygame.mixer.music.pause()


def music_resume() -> None:
    """
    Resume playing music if paused.

    **NOTE:**: Does nothing if pygame.mixer was not initialized.
    **NOTE:**: Does nothing if music volume is 0.
    """
    if pygame.mixer.get_init() is None or _music_vol <= 0.0:
        return

    pygame.mixer.music.unpause()


def music_stop() -> None:
    """
    Stop music if played.
    **NOTE:**: Does nothing if pygame.mixer was not initialized.
    **NOTE:**: Does nothing if music volume is 0.
    """
    if pygame.mixer.get_init() is None or _music_vol <= 0.0:
        return

    pygame.mixer.music.stop()

def sound_set_volume(volume: float) -> None:
    """
    Set sound volume. The value is always limited to 0.0-1.0.

    :param volume: new sound volume.
    """

    global _sound_vol
    _sound_vol = max(0.0, min(volume, 1.0))

    for sound in _sounds.values():
        sound.set_volume(_sound_vol)


def sound_get_volume() -> float|None:
    """
    Get sound volume.
    :return: current music volume.
    """
    return _sound_vol


def music_set_volume(volume: float) -> None:
    """
    Set the music volume. The value is always limited to 0.0-1.0.

    :param volume: new music volume.
    """

    new_vol: float = max(0.0, min(volume, 1.0))
    pygame.mixer.music.set_volume(new_vol)


def music_get_volume() -> float|None:
    """
    Get music volume.
    :return: current music volume.
    """
    return _music_vol


def to_dict() -> dict[str, Any]:
    """
    Pack audio configuration data into a dict (e.g. for saving into a config file).
    :return: key-value dict of audio configuration data.
    """
    return {
        'music_volume': _music_vol,
        'sound_volume': _sound_vol,
    }