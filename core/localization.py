from pathlib import Path
import yaml
from core import config

_DIR = "localization"
_FALLBACK_LANGUAGE = "English"

available_languages: dict[str, str] = {
    "English": "english.yml",
    "Russian": "russian.yml",
}

language: str = _FALLBACK_LANGUAGE
translation: dict[str, str] = {}

def load_translation(filename: str) -> None:
    global language, translation
    filename = Path(_DIR) / filename

    if not filename.exists():
        language = _FALLBACK_LANGUAGE
        filename = Path(_DIR) / available_languages[language]

    with open(filename, "r", encoding="utf-8") as file:
        translation = yaml.safe_load(file)


def change_language(new_lang: str) -> None:
    global language
    language = new_lang if new_lang in available_languages else _FALLBACK_LANGUAGE
    load_translation(available_languages[language])


def init(config_data) -> None:
    change_language(config_data["language"])


def translate(key: str) -> str:
    return translation.get(key, key)