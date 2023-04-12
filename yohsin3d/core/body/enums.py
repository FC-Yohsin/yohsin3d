from enum import Enum, IntEnum


class AgentType(IntEnum):
    NAO = 0
    NAO_HETERO_1 = 1
    NAO_HETERO_2 = 2
    NAO_HETERO_3 = 3
    NAO_HETERO_4 = 4


class BodyParts(Enum):
    TORSO = "TORSO"
    HEAD = "HEAD"
    ARM_LEFT = "ARM_LEFT"
    ARM_RIGHT = "ARM_RIGHT"
    LEG_LEFT = "LEG_LEFT"
    LEG_RIGHT = "LEG_RIGHT"
    FOOT_LEFT = "FOOT_LEFT"
    FOOT_RIGHT = "FOOT_RIGHT"
    TOE_LEFT = "TOE_LEFT"
    TOE_RIGHT = "TOE_RIGHT"
