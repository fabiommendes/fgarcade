from enum import IntFlag, IntEnum


class Command(IntFlag):
    NONE = 0
    LEFT = 1
    RIGHT = 2
    UP = 4
    DOWN = 8
    SPACE = 16


class Role(IntEnum):
    BACKGROUND = 0
    OBJECT = 1
    PLATFORM = 2
    RAMP_UP = 3
    RAMP_DOWN = 4