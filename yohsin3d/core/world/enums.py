
from enum import IntEnum, Enum


class Sides(IntEnum):
    LEFT = 0
    RIGHT = 1


class PlayModes(Enum):
    BEFORE_KICK_OFF = "BeforeKickOff"
    KICK_OFF_LEFT = "KickOff_Left"
    KICK_OFF_RIGHT = "KickOff_Right"
    PLAY_ON = "PlayOn"
    KICK_IN_LEFT = "KickIn_Left"
    KICK_IN_RIGHT = "KickIn_Right"
    GOAL_LEFT = "Goal_Left"
    GOAL_RIGHT = "Goal_Right"
    GAME_OVER = "GameOver"
    CORNER_KICK_LEFT = "corner_kick_left"
    CORNER_KICK_RIGHT = "corner_kick_right"
    GOAL_KICK_LEFT = "goal_kick_left"
    GOAL_KICK_RIGHT = "goal_kick_right"
    OFFSIDE_LEFT = "offside_left"
    OFFSIDE_RIGHT = "offside_right"
    FREE_KICK_LEFT = "free_kick_left"
    FREE_KICK_RIGHT = "free_kick_right"
    DIRECT_FREE_KICK_LEFT = "direct_free_kick_left"
    DIRECT_FREE_KICK_RIGHT = "direct_free_kick_right"
    PASS_LEFT = "pass_left"
    PASS_RIGHT = "pass_right"


class ForceResistancePerceptors(Enum):
    RF = 'rf'
    RF1 = 'rf1'
    LF = 'lf'
    LF1 = 'lf1'


class VisibleObjects(Enum):
    F1L = 'F1L'
    F1R = 'F1R'
    F2L = 'F2L'
    F2R = 'F2R'
    G1L = 'G1L'
    G1R = 'G1R'
    G2L = 'G2L'
    G2R = 'G2R'
    BALL = 'B'

    @property
    def global_position(self):
        return _WORLD_OBJECTS_GLOBAL_POSITIONS[self.name]


class WorldDimensions(Enum):
    HEIGHT = 20.0
    WIDTH = 30.0


_WORLD_OBJECTS_GLOBAL_POSITIONS = {
    "F1R": (15.0, 10.0, 0.0),
    "F1L": (-15.0, 10.0, 0.0),
    "F2R": (15.0, -10.0, 0.0),
    "F2L": (-15.0, -10.0, 0.0),
    "G1L": (-15.0, 1.05, 0.8),
    "G2L": (-15.0, -1.05, 0.8),
    "G1R": (15.0, 1.05, 0.8),
    "G2R": (15.0, -1.05, 0.8),
}
