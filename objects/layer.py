from enum import IntEnum


class Layer(IntEnum):
    BACKGROUND_3 = -3
    BACKGROUND_2 = -2
    BACKGROUND_1 = -1
    MAIN = 0
    FOREGROUND_1 = 1
    FOREGROUND_2 = 2
    GUI = 3