from typing import Any
import yaml

_FILENAME: str = "config.yml"


def read() -> dict[str, Any]:
    with open(_FILENAME, "r") as file:
        return yaml.safe_load(file)


def write(
    video: dict[str, Any],
    input: dict[str, Any],
    language: str,
) -> None:
    with open(_FILENAME, "w") as file:
        data: dict[str, Any] = {
            "video": video,
            "gui": {
                "language": language,
            },
            "input": input,
        }

        yaml.dump(data, file)
