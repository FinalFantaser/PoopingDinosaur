"""Tools for localization."""

from pathlib import Path
import yaml

_DIR: Path = Path("localization")
"""Path to the localization directory."""

_FALLBACK_LANGUAGE: str = "English"
"""Language to use as fallback in case if localization load failed."""

_available_languages: dict[str, str] = {}
"""List of available languages."""

_language: str = _FALLBACK_LANGUAGE
"""Current language."""

_translation: dict[str, str] = {}
"""Translation loaded as a key-value dictionary."""

def load_translation(filename: str) -> None:
    """
    Load translation from a file. If failed to load the file, fallback locale is used.

    The file must be in the "localization" directory.

    :param filename: name of the file to load.
    """
    global _language, _translation
    filename = _DIR / filename

    if not filename.exists():
        _language = _FALLBACK_LANGUAGE
        filename = _DIR / _available_languages[_language]

    with open(filename, "r", encoding="utf-8") as file:
        _translation = yaml.safe_load(file)


def change_language(new_lang: str) -> None:
    """
    Change game language.

    A translation file will be loaded instead of the previous one.

    :param new_lang: New language.
    :return:
    """
    global _language
    _language = new_lang if new_lang in _available_languages else _FALLBACK_LANGUAGE
    load_translation(_available_languages[_language])


def init(config_data) -> None:
    """
    Set the language specified in the config file and load a translation file.
    :param config_data: Data from the "video" section of the config file.
    """
    global _available_languages

    with open(_DIR / "_lang_.yml", "r", encoding="utf-8") as file:
        _available_languages = yaml.safe_load(file)

    change_language(config_data["language"])


def translate(key: str) -> str:
    """
    Get a translated text in current language.
    :param key: key of the text in localization file.
    :return: translated text or the key itself if the key was not found.
    """
    return _translation.get(key, key)