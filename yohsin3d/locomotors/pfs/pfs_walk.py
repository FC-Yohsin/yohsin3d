from ...core.common.constants import *
from ...core.common.joints import Joint
from ...core.body import BodyModel
from ...core.world import WorldModel
from ...core.localizer import BaseLocalizer
from ...movement import Movement
from .utility import Utility
import math
import numpy as np


WALK_INIT_SKILL = '''
start phase 0: 1.2
target lae1 -2.0 7.0
target rae1 -2.0 7.0
target lae2 -0.35 7.0
target rae2 -0.35 7.0
target lae3 -1.4 7.0
target rae3 1.4 7.0
target lae4 -0.52 7.0
target rae4 0.52 7.0
target lle1 0.15 7.0
target rle1 0.15 7.0
target lle2 -0.212 7.0
target rle2 0.212 7.0
target lle3 0.382 7.0
target rle3 0.382 7.0
target lle4 -0.5 7.0
target rle4 -0.5 7.0
target lle5 0.465 7.0
target rle5 0.465 7.0
target lle6 0.212 7.0
target rle6 -0.212 7.0
end phase
'''


class PFSWalk:
    def __init__(self,
                 body_model: BodyModel,
                 world_model: WorldModel,
                 localizer: BaseLocalizer,
                 ) -> None:
        self.body_model = body_model
        self.world_model = world_model
        self.localizer = localizer

        self.walk_counter = 0
        self.walk_init_skill: Movement = Movement.from_string(WALK_INIT_SKILL)
        self.should_get_ready = True
        self.stop_walk = False
        self.slow_down = False

    def get_ready_for_walk(self):
        if self.should_get_ready:
            self.walk_init_skill.perform(self.body_model, self.world_model)
            if self.walk_init_skill.is_finished():
                self.should_get_ready = False

    def get_walking_gain(self, counter):
        if 0 < counter < 20:
            return 5.0
        elif 20 <= counter < 40:
            return 6.0
        elif 40 <= counter < 60:
            return 7.0
        elif 60 <= counter < 80:
            return 8.0
        elif 80 <= counter < 100:
            return 9.0
        else:
            return 10.0

    def get_gain(self, distance_to_target, stop=True):
        if 3.5 <= distance_to_target < 4.0:
            return 8.0
        elif 3.0 <= distance_to_target < 3.5:
            self.slow_down = True
            return 7.0
        elif 2.5 <= distance_to_target < 3.0:
            return 6.5
        elif 2.0 <= distance_to_target < 2.5:
            return 6.35
        elif 1.5 <= distance_to_target < 2.0:
            return 6.25
        elif 1.0 <= distance_to_target < 1.5:
            return 6.0
        elif 0.7 <= distance_to_target < 1.0:
            return 5.5
        elif 0.5 <= distance_to_target < 0.7:
            return 5.0
        elif 0.3 <= distance_to_target < 0.5:
            return 4.5
        elif 0.2 <= distance_to_target < 0.3:
            return 4.0
        elif 0 < distance_to_target < 0.2:
            if stop:
                self.stop_walk = True
                self.should_get_ready = True
                self.walk_init_skill.reset()
            return None
        else:
            return self.get_walking_gain(self.walk_counter)

    def update_posture(self, gain):
        if not self.slow_down:
            if self.walk_counter < 100:
                self.body_model.set_target_angle(Joint.LA1, -60, gain)
                self.body_model.set_target_angle(Joint.RA1, -60, gain)
                self.body_model.set_target_angle(Joint.LA2, 0, gain)
                self.body_model.set_target_angle(Joint.RA2, 0, gain)

            else:
                self.body_model.set_target_angle(
                    Joint.LA1, math.degrees(-2.0), gain)
                self.body_model.set_target_angle(
                    Joint.RA1, math.degrees(-2.0), gain)
                self.body_model.set_target_angle(
                    Joint.LA2, math.degrees(0.35), gain)
                self.body_model.set_target_angle(
                    Joint.RA2, math.degrees(-0.35), gain)

            self.body_model.set_target_angle(
                Joint.LA3, math.degrees(-1.4), gain)
            self.body_model.set_target_angle(
                Joint.RA3, math.degrees(1.4), gain)
            self.body_model.set_target_angle(
                Joint.LA4, math.degrees(-0.52), gain)
            self.body_model.set_target_angle(
                Joint.RA4, math.degrees(0.52), gain)
        else:
            self.body_model.set_target_angle(
                Joint.LA1, math.degrees(-2.0), gain)
            self.body_model.set_target_angle(
                Joint.RA1, math.degrees(-2.0), gain)
            self.body_model.set_target_angle(
                Joint.LA2, math.degrees(0.35), gain)
            self.body_model.set_target_angle(
                Joint.RA2, math.degrees(-0.35), gain)
            self.body_model.set_target_angle(
                Joint.LA3, math.degrees(-1.4), gain)
            self.body_model.set_target_angle(
                Joint.RA3, math.degrees(1.4), gain)
            self.body_model.set_target_angle(
                Joint.LA4, math.degrees(-0.52), gain)
            self.body_model.set_target_angle(
                Joint.RA4, math.degrees(0.52), gain)

    def adjust_leg_joints(self, joints, target, t, T, dribble=False):

        my_position = self.localizer.my_location.position

        if not dribble:
            desired_orientation = math.radians(
                Utility.get_angle(target, my_position))
        else:
            desired_orientation = math.radians(self.dribbling_angle)

        current_orientation = math.radians(
            self.localizer.my_location.orientation)
        orientation_to_move = desired_orientation - current_orientation

        if (orientation_to_move < -math.pi):
            orientation_to_move = orientation_to_move + 2 * math.pi
        if desired_orientation < 0:
            desired_orientation = math.pi + (math.pi + desired_orientation)

        sharpness = 0.02

        x = 0.03 + 0.03 * math.sin(2 * math.pi * t / T - math.pi / 2 - 0.3)
        y = 0.03 + 0.03 * math.sin(2 * math.pi * t / T + math.pi / 2 - 0.3)

        if orientation_to_move < 0:
            llj2 = x - sharpness
            rlj2 = -y - sharpness

            llj6 = -y - sharpness
            rlj6 = x - sharpness

        elif orientation_to_move > 0:
            llj2 = x + sharpness
            rlj2 = -y + sharpness

            llj6 = -y + sharpness
            rlj6 = x + sharpness

        joints[Joint.LL2] = llj2
        joints[Joint.RL2] = rlj2
        joints[Joint.LL6] = llj6
        joints[Joint.RL6] = rlj6

        return joints

    def get_leg_joints(self, T, t):

        # Hip Yaw Pitch
        llj1 = -0.03
        rlj1 = -0.03

        # Hip Roll
        llj2 = 0.03
        rlj2 = -0.03

        # Hip Pitch
        llj3 = 0.382 + 0.75 * \
            math.sin(2 * math.pi * t / T - math.pi / 2 + 1.165)
        rlj3 = 0.382 + 0.72 * \
            math.sin(2 * math.pi * t / T + math.pi / 2 + 1.165)

        # Knee Pitch
        llj4 = -0.61 + 0.425 * \
            math.sin(2 * math.pi * t / T - math.pi / 2 - 1.115)
        rlj4 = -0.61 + 0.425 * \
            math.sin(2 * math.pi * t / T + math.pi / 2 - 1.115)

        # Foot Pitch
        llj5 = 0.465 + 0.425 * \
            math.sin(2 * math.pi * t / T + math.pi / 2 - 0.325)
        rlj5 = 0.465 + 0.425 * \
            math.sin(2 * math.pi * t / T - math.pi / 2 - 0.325)

        # Foot Roll
        llj6 = -0.03
        rlj6 = 0.03

        return {
            Joint.LL1: llj1,
            Joint.LL2: llj2,
            Joint.LL3: llj3,
            Joint.LL4: llj4,
            Joint.LL5: llj5,
            Joint.LL6: llj6,
            Joint.RL1: rlj1,
            Joint.RL2: rlj2,
            Joint.RL3: rlj3,
            Joint.RL4: rlj4,
            Joint.RL5: rlj5,
            Joint.RL6: rlj6
        }

    def adjust_desired_orientation(self, target):
        goal_mid_pos = (15.0, 0.0)
        my_position = self.localizer.my_location.position[:2]

        goal_pole_1 = WORLD_OBJECTS_GLOBAL_POSITIONS['G1R']
        goal_pole_2 = WORLD_OBJECTS_GLOBAL_POSITIONS['G2R']

        points = np.linspace(
            np.subtract(
                goal_pole_1, (0, 0.25, 0)), np.add(
                goal_pole_2, (0, 0.25, 0)), 5)

        if math.dist(my_position, goal_mid_pos) < 5:
            points = [goal_mid_pos]

        closest_theta = None
        closest_line_start_point = None
        lowest_turn_angle = 9999
        for point in points:
            goal_point = point[:2]
            line_start_point = Utility.get_point_on_goal_line(
                target, goal_point, -2.75)
            distance_to_point1 = math.dist(line_start_point, my_position)
            deviation_from_line = Utility.get_perpendicular_distance_to_line(
                target, goal_point, my_position)

            if target[1] > -1 and target[1] < 1 and target[0] > 14.8:
                theta = Utility.get_angle(target, my_position)
            elif distance_to_point1 > 0.1 and deviation_from_line > 0.5:
                theta = Utility.get_angle(line_start_point, my_position)
            else:
                theta = Utility.get_angle(target, my_position)

            turn_angle = abs(self.localizer.my_location.orientation - theta)

            if turn_angle < lowest_turn_angle:
                lowest_turn_angle = turn_angle
                closest_theta = theta
                closest_line_start_point = line_start_point

        self.dribbling_angle = closest_theta
        return closest_line_start_point

    def dribble_to_goal(self):
        target = self.localizer.ball_position[:2]
        target = self.adjust_desired_orientation(target)

        my_position = self.localizer.my_location.position[:2]
        distance = math.dist(my_position, target)
        self.get_ready_for_walk()

        if not self.should_get_ready and not self.stop_walk:
            self.walk_counter += 1
            T = 0.32
            t = self.walk_counter / 50
            gain = self.get_gain(distance, stop=False)
            self.update_posture(gain)
            joints = self.get_leg_joints(T, t)
            joints = self.adjust_leg_joints(joints, target, t, T, dribble=True)

            for joint in joints:
                self.body_model.set_target_angle(
                    joint, math.degrees(joints[joint]), gain)

    def walk_to(self, target):
        my_position = self.localizer.my_location.position[:2]
        distance = math.dist(my_position, target)
        self.get_ready_for_walk()

        if not self.should_get_ready and not self.stop_walk:
            self.walk_counter += 1
            T = 0.32
            t = self.walk_counter / 50
            gain = self.get_gain(distance)
            self.update_posture(gain)
            joints = self.get_leg_joints(T, t)
            joints = self.adjust_leg_joints(joints, target, t, T)

            for joint in joints:
                self.body_model.set_target_angle(
                    joint, math.degrees(joints[joint]), gain)
