from enum import Enum, IntEnum

class AgentType(IntEnum):
    AGENT_0 = 0
    AGENT_1 = 1
    AGENT_2 = 2
    AGENT_3 = 3
    AGENT_4 = 4

#  EffectorJoints
class EffectorJoints(IntEnum):
    EFF_H1 = 0 # Head Yaw
    EFF_H2 = 1 # Head Pitch

    EFF_LA1 = 2 # Left Arm Shoulder Pitch
    EFF_LA2 = 3 # Left Arm Shoulder Yaw
    EFF_LA3 = 4 # Left Arm Elbow Yaw
    EFF_LA4 = 5 # Left Arm Elbow Roll

    EFF_RA1 = 6 # Right Arm Shoulder Pitch
    EFF_RA2 = 7 # Right Arm Shoulder Yaw
    EFF_RA3 = 8 # Right Arm Elbow Yaw
    EFF_RA4 = 9 # Right Arm Elbow Roll

    EFF_LL1 = 10 # Left Leg Hip Yaw Pitch
    EFF_LL2 = 11 # Left Leg Hip Roll
    EFF_LL3 = 12 # Left Leg Hip Pitch
    EFF_LL4 = 13 # Left Leg Knee
    EFF_LL5 = 14 # Left Leg Pitch
    EFF_LL6 = 15 # Left Leg Roll
    EFF_LL7 = 16 # Left Leg Foot

    EFF_RL1 = 17 # Right Leg Hip Yaw Pitch
    EFF_RL2 = 18 # Right Leg Hip Roll
    EFF_RL3 = 19 # Right Leg Hip Pitch
    EFF_RL4 = 20 # Right Leg Knee
    EFF_RL5 = 21 # Right Leg Pitch
    EFF_RL6 = 22 # Right Leg Roll
    EFF_RL7 = 23 # Right Leg Foot

    def __str__(self):
        return self.name



# INDICES for body segments
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

    #  Number of agents on the team
    NUM_AGENTS = 11

    GAZEBO_AGENT_TYPE = -1


class Sensor(IntEnum):
    gyroX = 0
    gyroY = 1
    gyroZ = 2
    accelX = 3
    accelY = 4
    accelZ = 5
    battery = 6
    fsrLFL = 7
    fsrLFR = 8
    fsrLRL = 9
    fsrLRR = 10
    fsrRFL = 11
    fsrRFR = 12
    fsrRRL = 13
    fsrRRR = 14
    ultrasoundL = 15
    ultrasoundR = 16
    angleX = 17
    angleY = 18



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



class NaoRoles(IntEnum):
    GOALKEEPER = 0
    DEFENDER = 1
    MIDFIELDER = 2
    ATTACKER = 3


class LearnedSkills(IntEnum):
    STAND_SKILL = 0
    DRIBBLE_TO_GOAL = 1
    WALK_TO_TARGET = 2
    KICK_LEFT = 3
    KICK_RIGHT = 4
    WAVE_HANDS = 5
    GET_UP = 6
    FALL_ON_BELLY = 7
    FALL_ON_BACK = 8