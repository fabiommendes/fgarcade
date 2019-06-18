from enum import IntFlag, IntEnum


class Command(IntFlag):
    NONE = 0

    # Arrows
    LEFT = 1
    RIGHT = 2
    UP = 4
    DOWN = 8

    # Action
    SPACE = 16
    RETURN = 32

    # ASDW keys
    KEY_A = ASDW_LEFT = 64
    KEY_D = ASDW_RIGHT = 128
    KEY_S = ASDW_DOWN = 256
    KEY_W = ASDW_UP = 512



class Role(IntEnum):
    BACKGROUND = 0
    FOREGROUND = 1
    OBJECT = 2
    PLATFORM = 3
    RAMP_UP = 4
    RAMP_DOWN = 5