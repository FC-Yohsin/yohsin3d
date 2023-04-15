from enum import IntEnum
from ...core.body import BodyModel
from ...core.common import Joint
from ...core.world import WorldModel
from ...core.localizer import BaseLocalizer
from ...movement import Movement
import math


STAND_SKILL = '''
start phase 0: 2.0
target lle1 0 5.0
target rle1 0 5.0
target lle2 5 5.0
target rle2 -5 5.0
target lle3 25 5.0
target rle3 25 5.0
target lle4 -65 5.0
target rle4 -65 5.0
target lle5 36 5.0
target rle5 36 5.0
target lle6 -1 5.0
target rle6 1 5.0
target lae1 -75 5.0
target rae1 -75 5.0
target lae2 45 5.0
target rae2 -45 5.0
target lae4 -68 5.0
target rae4 68 5.0
target lle1 -11 5.0
target rle1 -11 5.0
end phase
'''


class TurnDirection(IntEnum):
    LEFT = 0
    RIGHT = 1


class PFSTurn:
    def __init__(
            self,
            body_model: BodyModel,
            world_model: WorldModel,
            localizer: BaseLocalizer) -> None:
        self.body_model = body_model
        self.world_model = world_model
        self.localizer = localizer
        self.stand_skill: Movement = Movement.from_string(STAND_SKILL)
        self.turn_counter = 0

        self.turn_reset_skills = False
        self.turn_finished = False

    def execute_turn_orientation(self, theta):

        current_orientation = self.localizer.my_location.orientation

        direction = None
        if theta < current_orientation:
            direction = TurnDirection.RIGHT

        elif theta > current_orientation:
            direction = TurnDirection.LEFT

        if not self.turn_finished:
            self.turn_counter += 1
            self.turn_to(desired_orientation=theta,
                         turn_direction=direction)
        else:
            if self.turn_reset_skills:
                self.stand_skill.reset()
                self.turn_reset_skills = False

            self.stand_skill.perform(self.body_model, self.world_model)

    def get_turning_gain(self):

        if (0 <= self.turn_counter < 20):
            return 1.0

        elif (20 <= self.turn_counter < 40):
            return 3.0

        elif (40 <= self.turn_counter < 60):
            return 5.0

        elif (60 <= self.turn_counter < 80):
            return 5.0

        elif (80 <= self.turn_counter < 100):
            return 6.0
        else:
            return 7.0

    def get_gain(self, desired_orientation):

        current_orientation = self.localizer.my_location.orientation
        difference = abs(desired_orientation - current_orientation)

        if 15 <= difference < 20:
            return 5.0
        elif 10 <= difference < 15:
            return 4.5
        elif 8 <= difference < 10:
            return 3.5
        elif 7 <= difference < 8:
            return 2.5
        elif 5 <= difference < 6:
            return 1.25
        elif difference < 5:
            self.turn_finished = True
            return
        else:
            return self.get_turning_gain()

    def update_posture(self, gain):
        self.body_model.set_target_angle(Joint.LA1, math.degrees(-2.0), gain)
        self.body_model.set_target_angle(Joint.RA1, math.degrees(-2.0), gain)
        self.body_model.set_target_angle(Joint.LA2, math.degrees(0.35), gain)
        self.body_model.set_target_angle(Joint.LA2, math.degrees(-0.35), gain)
        self.body_model.set_target_angle(Joint.LA3, math.degrees(-1.4), gain)
        self.body_model.set_target_angle(Joint.RA3, math.degrees(1.4), gain)
        self.body_model.set_target_angle(Joint.LA4, math.degrees(-0.52), gain)
        self.body_model.set_target_angle(Joint.RA4, math.degrees(0.52), gain)

    def get_leg_joints(self, turn_direction):

        T = -0.26
        t = self.turn_counter / 50

        llj1 = -0.05 - 0.18 * \
            math.sin(2 * math.pi * t / T + 2.575)    # Hip Yaw Pitch
        rlj1 = llj1

        # Hip Pitch
        llj3 = 0.515
        rlj3 = 0.4

        # Hip Roll
        llj2 = 0.126 + 0.4 * \
            math.sin(2 * math.pi * t / T + 0.435)    # hip roll
        rlj2 = -0.2 + 0.4 * math.sin(2 * math.pi * t / T - 1.7)

        # Knee Pitch
        llj4 = -0.71
        rlj4 = -0.39 + 0.265 * math.sin(2 * math.pi * t / T - 0.37)

        # Foot Pitch
        llj5 = 0.4
        rlj5 = 0.255

        # ankle roll
        llj6 = -0.015 - 0.25 * math.sin(2 * math.pi * t / T + 2.215)
        rlj6 = 0.675 + 0.56 * math.sin(2 * math.pi * t / T - 1.69)

        if turn_direction == TurnDirection.LEFT:

            llj1, rlj1 = rlj1, llj1
            llj3, rlj3 = rlj3, llj3
            llj2, rlj2 = -rlj2, -llj2
            llj4, rlj4 = rlj4, llj4
            llj5, rlj5 = rlj5, llj5
            llj6, rlj6 = -rlj6, -llj6

        return {
            Joint.LL1: llj1,
            Joint.LL2: llj2,
            Joint.LL3: llj3,
            Joint.LL4: llj4,
            Joint.LL5: llj5,
            Joint.LL6: llj6,
        }

    def turn_to(self, desired_orientation, turn_direction: TurnDirection):
        gain = self.get_gain(desired_orientation)

        self.update_posture(gain)
        joints = self.get_leg_joints(turn_direction)
        for joint, angle in joints.items():
            self.body_model.set_target_angle(joint, math.degrees(angle), gain)

    def reset(self):
        self.turn_counter = 0
        self.turn_finished = False
        self.turn_reset_skills = True
