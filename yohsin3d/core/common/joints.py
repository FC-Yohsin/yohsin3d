from enum import IntEnum
from typing import Tuple

#  Effector Joints


class Joint(IntEnum):
    H1 = 0  # Head Yaw
    H2 = 1  # Head Pitch

    LA1 = 2  # Left Arm Shoulder Pitch
    LA2 = 3  # Left Arm Shoulder Yaw
    LA3 = 4  # Left Arm Elbow Yaw
    LA4 = 5  # Left Arm Elbow Roll

    RA1 = 6  # Right Arm Shoulder Pitch
    RA2 = 7  # Right Arm Shoulder Yaw
    RA3 = 8  # Right Arm Elbow Yaw
    RA4 = 9  # Right Arm Elbow Roll

    LL1 = 10  # Left Leg Hip Yaw Pitch
    LL2 = 11  # Left Leg Hip Roll
    LL3 = 12  # Left Leg Hip Pitch
    LL4 = 13  # Left Leg Knee
    LL5 = 14  # Left Leg Pitch
    LL6 = 15  # Left Leg Roll
    LL7 = 16  # Left Leg Foot

    RL1 = 17  # Right Leg Hip Yaw Pitch
    RL2 = 18  # Right Leg Hip Roll
    RL3 = 19  # Right Leg Hip Pitch
    RL4 = 20  # Right Leg Knee
    RL5 = 21  # Right Leg Pitch
    RL6 = 22  # Right Leg Roll
    RL7 = 23  # Right Leg Foot

    def __str__(self):
        return self.name

    @property
    def range(self) -> Tuple[float, float]:
        return joint_to_range[self]

    @property
    def effector_name(self) -> str:
        return joint_to_effector[self]


joint_to_range = {
    Joint.H1: (-120.0, 120.0),
    Joint.H2: (-45.0, 45.0),

    Joint.LA1: (-120.0, 120.0),
    Joint.LA2: (-1.0, 95.0),
    Joint.LA3: (-120.0, 120.0),
    Joint.LA4: (-90.0, 1.0),

    Joint.RA1: (-120.0, 120.0),
    Joint.RA2: (-95.0, 1.0),
    Joint.RA3: (-120.0, 120.0),
    Joint.RA4: (-1.0, 90.0),

    Joint.LL1: (-90.0, 1.0),
    Joint.LL2: (-25.0, 45.0),
    Joint.LL3: (-25.0, 100.0),
    Joint.LL4: (-130.0, 1.0),
    Joint.LL5: (-45.0, 75.0),
    Joint.LL6: (-45.0, 25.0),
    Joint.LL7: (-1.0, 70.0),

    Joint.RL1: (-90.0, 1.0),
    Joint.RL2: (-45.0, 25.0),
    Joint.RL3: (-25.0, 100.0),
    Joint.RL4: (-130.0, 1.0),
    Joint.RL5: (-45.0, 75.0),
    Joint.RL6: (-25.0, 45.0),
    Joint.RL7: (-1.0, 70.0),
}


joint_to_effector = {
    Joint.H1: "he1",
    Joint.H2: "he2",
    Joint.LA1: "lae1",
    Joint.LA2: "lae2",
    Joint.LA3: "lae3",
    Joint.LA4: "lae4",

    Joint.RA1: "rae1",
    Joint.RA2: "rae2",
    Joint.RA3: "rae3",
    Joint.RA4: "rae4",

    Joint.LL1: "lle1",
    Joint.LL2: "lle2",
    Joint.LL3: "lle3",
    Joint.LL4: "lle4",
    Joint.LL5: "lle5",
    Joint.LL6: "lle6",
    Joint.LL7: "lle7",

    Joint.RL1: "rle1",
    Joint.RL2: "rle2",
    Joint.RL3: "rle3",
    Joint.RL4: "rle4",
    Joint.RL5: "rle5",
    Joint.RL6: "rle6",
    Joint.RL7: "rle7",
}

effector_to_joint = {v: k for k, v in joint_to_effector.items()}


perceptor_to_joint = {
    "hj1": Joint.H1,
    "hj2": Joint.H2,
    "laj1": Joint.LA1,
    "laj2": Joint.LA2,
    "laj3": Joint.LA3,
    "laj4": Joint.LA4,

    "raj1": Joint.RA1,
    "raj2": Joint.RA2,
    "raj3": Joint.RA3,
    "raj4": Joint.RA4,

    "llj1": Joint.LL1,
    "llj2": Joint.LL2,
    "llj3": Joint.LL3,
    "llj4": Joint.LL4,
    "llj5": Joint.LL5,
    "llj6": Joint.LL6,
    "llj7": Joint.LL7,

    "rlj1": Joint.RL1,
    "rlj2": Joint.RL2,
    "rlj3": Joint.RL3,
    "rlj4": Joint.RL4,
    "rlj5": Joint.RL5,
    "rlj6": Joint.RL6,
    "rlj7": Joint.RL7,
}
