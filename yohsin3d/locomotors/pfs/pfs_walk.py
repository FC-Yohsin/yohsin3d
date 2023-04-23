from ...core.common.constants import *
from ...core.common.joints import Joint
from ...core.body import BodyModel
from ...core.world import WorldModel
from ...core.localizer import BaseLocalizer
from ...movement import Movement
from .pfs_turn import PFSTurn
from .utility import Utility
from ...drawing import RvDraw
import math
from enum import Enum


WALK_INIT_SKILL = '''
start phase 0: 0.7
target lle1 0 7.0
target rle1 0 7.0
target lle2 5 7.0
target rle2 -5 5.0
target lle3 25 6.0
target rle3 25 6.0
target lle4 -65 5.0
target rle4 -65 5.0
target lle5 36 5.0
target rle5 36 6.0
target lle6 -1 6.0
target rle6 1 6.0
target lae1 -75 5.0
target rae1 -75 6.0
target lae2 45 6.0
target rae2 -45 5.0
target lae4 -68 6.0
target rae4 68 5.0
target lle1 -11 5.0
target rle1 -11 5.0
end phase
'''


# Sequential States
class States(Enum):
    TESTING = -1
    DRIBBLE_BALL_TO_GOAL = 0
    WALK_BEHIND_BALL = 1
    TURNING_TO_BALL = 2

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

        self.drawer = RvDraw()
        self.pfs_turn = PFSTurn(self.body_model, self.world_model, self.localizer)

        self.last_state =  None
        self.current_state = States.TESTING
        

    def get_ready_for_walk(self):
        if self.should_get_ready:
            self.walk_init_skill.perform(self.body_model, self.world_model)
            if self.walk_init_skill.is_finished():
                self.should_get_ready = False

                if self.current_state == States.WALK_BEHIND_BALL:
                    self.current_state = States.TURNING_TO_BALL

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
            return 7.0
        elif 2.5 <= distance_to_target < 3.0:
            return 6.5
        elif 2.0 <= distance_to_target < 2.5:
            return 6.5
        elif 1.5 <= distance_to_target < 2.0:
            return 6.25
        elif 1.3 <= distance_to_target < 1.5:
            return 6.0
        elif 1.0 <= distance_to_target < 1.3:
            return 5.5
        elif 0.7 <= distance_to_target < 1.0:
            return 5.25
        elif 0.5 <= distance_to_target < 0.7:
            return 5.0
        elif 0.3 <= distance_to_target < 0.5:
            return 4.5
        elif 0.2 <= distance_to_target < 0.3:
            return 4.0
        elif distance_to_target < 0.2:
            if stop:
                if self.current_state == States.WALK_BEHIND_BALL:
                    self.walk_counter = 0
                    self.stop_walk = True
                    self.should_get_ready = True
                    self.walk_init_skill.reset()
            return 3.0
        else:
            return self.get_walking_gain(self.walk_counter)
        
    def get_arm_joints(self, joints):
        if self.walk_counter < 100:
            joints[Joint.LA1] = math.radians(-60)
            joints[Joint.RA1] = math.radians(-60)
            joints[Joint.LA2] = math.radians(0)
            joints[Joint.RA2] = math.radians(0)

        else:
            joints[Joint.LA1] = -2.0
            joints[Joint.RA1] = -2.0
            joints[Joint.LA2] = 0.35
            joints[Joint.RA2] = -0.35

        joints[Joint.LA3] = -1.4
        joints[Joint.RA3] = 1.4
        joints[Joint.LA4] = -0.52
        joints[Joint.RA4] = 0.52
        
        return joints


    def update_posture(self, gain):

        joints = {
            Joint.LA1: None,
            Joint.LA2: None,
            Joint.LA3: None,
            Joint.LA4: None,

            Joint.RA1: None,
            Joint.RA2: None,
            Joint.RA3: None,
            Joint.RA4: None,
        }

        joints = self.get_arm_joints(joints)

        for joint in joints:
            angle = joints[joint]
            if angle is not None:
                self.body_model.set_target_angle(joint, angle, gain, True)

    def adjust_leg_joints(self, joints, target, t, T, dribble=False):

        my_position = self.localizer.my_location.position

        if not dribble:
            angle_to_ball = Utility.get_angle(target, my_position)
            desired_orientation = math.radians(angle_to_ball)
        else:
            desired_orientation = math.radians(self.dribbling_angle)

        current_orientation = math.radians(self.localizer.my_location.orientation)
        orientation_to_move = desired_orientation - current_orientation

        if (orientation_to_move < -math.pi):
            orientation_to_move = orientation_to_move + 2 * math.pi
        if desired_orientation < 0:
            desired_orientation = math.pi + (math.pi + desired_orientation)

        sharpness = 0.020

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
        my_position = self.localizer.my_location.position[:2]
        goal_point = GOAL_MID_POSITION
        point_behind_ball = Utility.get_point_on_goal_line(target, goal_point, -2.80)
        distance = math.dist(point_behind_ball, my_position)
        deviation = Utility.get_perpendicular_distance_to_line(target, goal_point, my_position)

        if distance > 0.1 and deviation > 0.5: target = point_behind_ball
        theta = Utility.get_angle(target, my_position)
        self.dribbling_angle = theta
        return target


    def turn_to_ball(self):
        ball_position = self.localizer.ball_position[:2]
        my_position = self.localizer.my_location.position[:2]
        theta = Utility.get_angle(ball_position, my_position)
        turn_finished = self.pfs_turn.execute_turn_orientation(theta)

        if turn_finished == True:
            self.walk_counter = 0
            self.current_state = States.DRIBBLE_BALL_TO_GOAL


    def dribble_walk(self):

        my_position = self.localizer.my_location.position[:2]
        ball_position = self.localizer.ball_position[:2]

        if my_position[0] > ball_position[0]:
            self.current_state = States.WALK_BEHIND_BALL

        if self.current_state == States.TESTING:
            self.walk_to((3,3))
        elif self.current_state == States.DRIBBLE_BALL_TO_GOAL:
            self.dribble_to_goal()
        elif self.current_state == States.WALK_BEHIND_BALL:
            point_behind_ball = Utility.get_point_on_goal_line(ball_position, GOAL_MID_POSITION, -1.75)
            self.walk_to(point_behind_ball)
        elif self.current_state == States.TURNING_TO_BALL:
            self.turn_to_ball()
            

    def walk_to(self, target, dribble_ball=False):
        my_position = self.localizer.my_location.position[:2]
        distance = math.dist(my_position, target)
        self.get_ready_for_walk()

        if dribble_ball and self.current_state == States.DRIBBLE_BALL_TO_GOAL:
            self.stop_walk = False

        if not self.should_get_ready and not self.stop_walk:
            self.walk_counter += 1
            T = 0.32
            t = self.walk_counter / 50
            gain = self.get_gain(distance, stop=(not dribble_ball))
            self.update_posture(gain)
            joints = self.get_leg_joints(T, t)
            joints = self.adjust_leg_joints(joints, target, t, T, dribble=dribble_ball)

            for joint in joints:
                angle = joints[joint]
                angle = math.degrees(angle)
                self.body_model.set_target_angle(joint, angle, gain)


    def dribble_to_goal(self):
        target = self.localizer.ball_position[:2]
        target = self.adjust_desired_orientation(target)
        self.walk_to(target, dribble_ball=True)
                

    def reset(self):
        self.walk_counter = 0
        self.pfs_turn.reset()
