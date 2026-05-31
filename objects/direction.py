from enum import Enum
from typing import Literal, Self


class Direction(Enum):
    UP = 0, 1
    DOWN = 0, -1
    LEFT = -1, 0
    RIGHT = 1, 0

    def __str__(self) -> Literal["UP", "DOWN", "LEFT", "RIGHT", "UNKNOWN"]:
        if self.value == self.UP.value:
            return 'UP'
        elif self.value == self.DOWN.value:
            return 'DOWN'
        elif self.value == self.LEFT.value:
            return 'LEFT'
        elif self.value == self.RIGHT.value:
            return 'RIGHT'
        else:
            return 'UNKNOWN'

    def opposite(self) -> Self:
        if self.value == self.UP.value:
            return self.DOWN
        elif self.value == self.DOWN.value:
            return self.UP
        elif self.value == self.LEFT.value:
            return self.RIGHT
        elif self.value == self.RIGHT.value:
            return self.LEFT
        else:
            raise ValueError('Unknown direction value')