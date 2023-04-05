
from enum import IntEnum, Enum

SIDE_LEFT = 0
SIDE_RIGHT = 1

class PlayModes(IntEnum):
    # Play Modes
    PM_BEFORE_KICK_OFF = 0
    PM_KICK_OFF_LEFT = 1
    PM_KICK_OFF_RIGHT = 2
    PM_PLAY_ON = 3
    PM_KICK_IN_LEFT = 4
    PM_KICK_IN_RIGHT = 5
    PM_GOAL_LEFT = 6
    PM_GOAL_RIGHT = 7
    PM_GAME_OVER = 8

    # Extra added.
    PM_CORNER_KICK_LEFT = 9
    PM_CORNER_KICK_RIGHT = 10
    PM_GOAL_KICK_LEFT = 11
    PM_GOAL_KICK_RIGHT = 12
    PM_OFFSIDE_LEFT = 13
    PM_OFFSIDE_RIGHT = 14
    PM_FREE_KICK_LEFT = 15
    PM_FREE_KICK_RIGHT = 16
    PM_DIRECT_FREE_KICK_LEFT = 17
    PM_DIRECT_FREE_KICK_RIGHT = 18
    PM_PASS_LEFT = 19
    PM_PASS_RIGHT = 20


playModeStringToEnum = {
    "BeforeKickOff": PlayModes.PM_BEFORE_KICK_OFF,
    "KickOff_Left": PlayModes.PM_KICK_OFF_LEFT,
    "KickOff_Right": PlayModes.PM_KICK_OFF_RIGHT,
    "PlayOn": PlayModes.PM_PLAY_ON,
    "KickIn_Left": PlayModes.PM_KICK_IN_LEFT,
    "KickIn_Right": PlayModes.PM_KICK_IN_RIGHT,
    "Goal_Left": PlayModes.PM_GOAL_LEFT,
    "Goal_Right": PlayModes.PM_GOAL_RIGHT,
    "GameOver": PlayModes.PM_GAME_OVER,
    "corner_kick_left": PlayModes.PM_CORNER_KICK_LEFT,
    "corner_kick_right": PlayModes.PM_CORNER_KICK_RIGHT,
    "goal_kick_left": PlayModes.PM_GOAL_KICK_LEFT,
    "goal_kick_right": PlayModes.PM_GOAL_KICK_RIGHT,
    "offside_left": PlayModes.PM_OFFSIDE_LEFT,
    "offside_right": PlayModes.PM_OFFSIDE_RIGHT,
    "free_kick_left": PlayModes.PM_FREE_KICK_LEFT,
    "free_kick_right": PlayModes.PM_FREE_KICK_RIGHT,
    "direct_free_kick_left": PlayModes.PM_DIRECT_FREE_KICK_LEFT,
    "direct_free_kick_right": PlayModes.PM_DIRECT_FREE_KICK_RIGHT,
    "pass_left": PlayModes.PM_PASS_LEFT,
    "pass_right": PlayModes.PM_PASS_RIGHT,
}



class VisibleObjects(Enum):
    F1L = 'F1L'
    F1R = 'F1R'
    F2L = 'F2L'
    F2R = 'F2R'
    G1L = 'G1L'
    G1R = 'G1R'
    G2L = 'G2L'
    G2R = 'G2R'
    B = 'B'


class WorldDimensions(Enum):
    HEIGHT = 20.0
    WIDTH = 30.0
