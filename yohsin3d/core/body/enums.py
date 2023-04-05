from enum import Enum, IntEnum



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
    
    def to_range(self):
        return effector_to_range[self]
    
    def to_string(self):
        return effector_to_string[self]



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