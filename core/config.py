"""Tools for reading and writing config files."""

from typing import Any
import yaml

_FILENAME: str = "config.yml"
"""Config file name."""

def read() -> dict[str, Any]:
    """
    Load config file.
    :return: Loaded config as a key -> value dict.
    """
    with open(_FILENAME, "r") as file:
        return yaml.safe_load(file)


def write(
    video: dict[str, Any],
    input: dict[str, Any],
    language: str,
) -> None:
    """
    Write config into a file.
    :param video: video config data.
    :param input: input config data.
    :param language: game language.
    """
    with open(_FILENAME, "w") as file:
        data: dict[str, Any] = {
            "video": video,
            "gui": {
                "language": language,
            },
            "input": input,
        }

        yaml.dump(data, file)
