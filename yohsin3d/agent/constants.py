from enums import *

USE_GROUND_TRUTH = True

joint_to_effector = {
    "hj1": EffectorJoints.EFF_H1,
    "hj2": EffectorJoints.EFF_H2,
    "laj1": EffectorJoints.EFF_LA1,
    "laj2": EffectorJoints.EFF_LA2,
    "laj3": EffectorJoints.EFF_LA3,
    "laj4": EffectorJoints.EFF_LA4,

    "raj1": EffectorJoints.EFF_RA1,
    "raj2": EffectorJoints.EFF_RA2,
    "raj3": EffectorJoints.EFF_RA3,
    "raj4": EffectorJoints.EFF_RA4,

    "llj1": EffectorJoints.EFF_LL1,
    "llj2": EffectorJoints.EFF_LL2,
    "llj3": EffectorJoints.EFF_LL3,
    "llj4": EffectorJoints.EFF_LL4,
    "llj5": EffectorJoints.EFF_LL5,
    "llj6": EffectorJoints.EFF_LL6,
    "llj7": EffectorJoints.EFF_LL7,

    "rlj1": EffectorJoints.EFF_RL1,
    "rlj2": EffectorJoints.EFF_RL2,
    "rlj3": EffectorJoints.EFF_RL3,
    "rlj4": EffectorJoints.EFF_RL4,
    "rlj5": EffectorJoints.EFF_RL5,
    "rlj6": EffectorJoints.EFF_RL6,
    "rlj7": EffectorJoints.EFF_RL7,
}

left_to_right = {
    EffectorJoints.EFF_LA1: EffectorJoints.EFF_RA1,
    EffectorJoints.EFF_LA2: EffectorJoints.EFF_RA2,
    EffectorJoints.EFF_LA3: EffectorJoints.EFF_RA3,
    EffectorJoints.EFF_LA4: EffectorJoints.EFF_RA4,

    EffectorJoints.EFF_LL1: EffectorJoints.EFF_RL1,
    EffectorJoints.EFF_LL2: EffectorJoints.EFF_RL2,
    EffectorJoints.EFF_LL3: EffectorJoints.EFF_RL3,
    EffectorJoints.EFF_LL4: EffectorJoints.EFF_RL4,
    EffectorJoints.EFF_LL5: EffectorJoints.EFF_RL5,
    EffectorJoints.EFF_LL6: EffectorJoints.EFF_RL6,
    EffectorJoints.EFF_LL7: EffectorJoints.EFF_RL7,
}

right_to_left = {v: k for k, v in left_to_right.items()}


effector_to_string = {
    EffectorJoints.EFF_H1: "he1",
    EffectorJoints.EFF_H2: "he2",
    EffectorJoints.EFF_LA1: "lae1",
    EffectorJoints.EFF_LA2: "lae2",
    EffectorJoints.EFF_LA3: "lae3",
    EffectorJoints.EFF_LA4: "lae4",

    EffectorJoints.EFF_RA1: "rae1",
    EffectorJoints.EFF_RA2: "rae2",
    EffectorJoints.EFF_RA3: "rae3",
    EffectorJoints.EFF_RA4: "rae4",

    EffectorJoints.EFF_LL1: "lle1",
    EffectorJoints.EFF_LL2: "lle2",
    EffectorJoints.EFF_LL3: "lle3",
    EffectorJoints.EFF_LL4: "lle4",
    EffectorJoints.EFF_LL5: "lle5",
    EffectorJoints.EFF_LL6: "lle6",
    EffectorJoints.EFF_LL7: "lle7",

    EffectorJoints.EFF_RL1: "rle1",
    EffectorJoints.EFF_RL2: "rle2",
    EffectorJoints.EFF_RL3: "rle3",
    EffectorJoints.EFF_RL4: "rle4",
    EffectorJoints.EFF_RL5: "rle5",
    EffectorJoints.EFF_RL6: "rle6",
    EffectorJoints.EFF_RL7: "rle7",
}

string_to_effector = {v: k for k, v in effector_to_string.items()}

effector_to_range = {
    EffectorJoints.EFF_H1: (-120.0, 120.0),
    EffectorJoints.EFF_H2: (-45.0, 45.0),

    EffectorJoints.EFF_LA1: (-120.0, 120.0),
    EffectorJoints.EFF_LA2: (-1.0, 95.0),
    EffectorJoints.EFF_LA3: (-120.0, 120.0),
    EffectorJoints.EFF_LA4: (-90.0, 1.0),

    EffectorJoints.EFF_RA1: (-120.0, 120.0),
    EffectorJoints.EFF_RA2: (-95.0, 1.0),
    EffectorJoints.EFF_RA3: (-120.0, 120.0),
    EffectorJoints.EFF_RA4: (-1.0, 90.0),

    EffectorJoints.EFF_LL1: (-90.0, 1.0),
    EffectorJoints.EFF_LL2: (-25.0, 45.0),
    EffectorJoints.EFF_LL3: (-25.0, 100.0),
    EffectorJoints.EFF_LL4: (-130.0, 1.0),
    EffectorJoints.EFF_LL5: (-45.0, 75.0),
    EffectorJoints.EFF_LL6: (-45.0, 25.0),
    EffectorJoints.EFF_LL7: (-1.0, 70.0),

    EffectorJoints.EFF_RL1: (-90.0, 1.0),
    EffectorJoints.EFF_RL2: (-45.0, 25.0),
    EffectorJoints.EFF_RL3: (-25.0, 100.0),
    EffectorJoints.EFF_RL4: (-130.0, 1.0),
    EffectorJoints.EFF_RL5: (-45.0, 75.0),
    EffectorJoints.EFF_RL6: (-25.0, 45.0),
    EffectorJoints.EFF_RL7: (-1.0, 70.0),
}


def getEffector(effectorString):
    for eff in EffectorJoints:
        if eff.name == effectorString:
            return eff


# Flags
FLAG_NUM = 4

# Goal Posts
GOALPOST_NUM = 4

# Team Playing Side
SIDE_LEFT = 0
SIDE_RIGHT = 1

TEAMMATE_NUM = 11
OPPONENT_NUM = 11


FIELD_Y = 20
FIELD_X = 30

HALF_FIELD_Y = FIELD_Y / 2.0
HALF_FIELD_X = FIELD_X / 2.0

GOAL_Y = 2.1  # width
GOAL_X = .6  # depth
GOAL_Z = .8  # height
HALF_GOAL_Y = GOAL_Y / 2.0

PENALTY_Y = 6.0
PENALTY_X = 1.8

FIELD_CENTER_X = 0
FIELD_CENTER_Y = 0

CORNER_Y = 5.5


visible_objects = {
    "F1L": None,
    "F2L": None,
    "F1R": None,
    "F2R": None,
    "G1L": None,
    "G2L": None,
    "G1R": None,
    "G2R": None,
    "B": None,
    "L": None,
}

force_resistance_perceptors = {'rf': None, 'lf': None}

WORLD_OBJECTS_GLOBAL_POSITIONS = {
    "F1R": (15.0, 10.0, 0.0),
    "F1L": (-15.0, 10.0, 0.0),
    "F2R": (15.0, -10.0, 0.0),
    "F2L": (-15.0, -10.0, 0.0),
    "G1L": (-15.0, 1.05, 0.8),
    "G2L": (-15.0, -1.05, 0.8),
    "G1R": (15.0, 1.05, 0.8),
    "G2R": (15.0, -1.05, 0.8),
}


BEFORE_KICKOFF_FORMATION_LEFT = {
    1 : (-14.4, 0.0), # Goalie
    2 :  (-11.0, 5.5), # Defender left
    3 : (-11.0, -5.5), # Defender right
    4 : (-0.65, 7.0), # Midfielder left
    5 : (-0.65, -7.0), # Midfielder right
    6 : (-7.5, -3.2),  # Forward left
    7 : (-7.5, 3.2), # Forward right
    8 : (-5.8, 0.0), # Striker
    9 : (-5, 7),  # Supporter left
    10 : (-5, -7), # Supporter right
    11 : (-2.3, 0.0), # Supporter center
}




# During the game place the robot uniformly in the field
# Field size is 30x20
PLAYON_POSITIONS_LEFT = {
    1 : (-14.4, 0.0), 
    2 :  (-12.0, 2.5),  
    3 : (-12.0, -2.5), 
    4 : (-8, 7), 
    5 : (-8, -7), 
    6 : (0, 4),  
    7 : (0, -4),
    8 : (2, 0.0), 
    9 : (10, 6), 
    10 : (10,-6), 
    11 : (12.5, 0),  
}




class NaoRoles(IntEnum):
    GOALIE = 0
    DEFENDER = 1
    MIDFIELDER = 2
    FORWARD = 3
    ATTACKER = 4


unumToRole = {
    1 : NaoRoles.GOALIE,
    2 : NaoRoles.DEFENDER,
    3 : NaoRoles.DEFENDER,
    4 : NaoRoles.ATTACKER,
    5 : NaoRoles.ATTACKER,
    6 : NaoRoles.FORWARD,
    7 : NaoRoles.FORWARD,
    8 : NaoRoles.ATTACKER,
    9 : NaoRoles.ATTACKER,
    10 : NaoRoles.MIDFIELDER,
    11 : NaoRoles.MIDFIELDER,
}

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





