
import math
from .enums import *
from .nao_joint import NaoJoint
from ..world.world_model import WorldModel
from ..common import Joint

from typing import List


class BodyModel:
    def __init__(self, worldModel: WorldModel) -> None:
        self.gyro_rates = (0, 0, 0)
        self.prev_gyro_rates = (0, 0, 0)
        self.accel_rates = (0, 0, 0)
        self.walk_angle = None
        self.agent_type = None

        self.world_model = worldModel
        self.joints_list: List[NaoJoint] = [
            None for _ in range(len(Joint))
        ]

        self.previous_joints_list: list[NaoJoint] = [
            None for _ in range(len(Joint))
        ]

        self.initialise_joints()

    def set_initial_head(self):

        gain = 7.0
        self.set_target_angle(Joint.H1, 0, gain)
        self.set_target_angle(Joint.H2, -45, gain)

    def target_reached(self, joint: Joint):
        return abs(self.joints_list[joint].current_angle -
                   self.joints_list[joint].target_angle
                   ) < self.joints_list[joint].error_tolerance

    def set_initial_arm(self, arm) -> bool:

        ang1 = -50.0
        ang2 = 30.0
        ang3 = 0
        ang4 = -50.0

        gain = 7.0

        if (arm == BodyParts.ARM_LEFT):

            self.set_target_angle(Joint.LA1, ang1, gain)
            self.set_target_angle(Joint.LA2, ang2, gain)
            self.set_target_angle(Joint.LA3, ang3, gain)
            self.set_target_angle(Joint.LA4, ang4, gain)

        else:

            self.set_target_angle(Joint.RA1, ang1, gain)
            self.set_target_angle(Joint.RA2, -ang2, gain)
            self.set_target_angle(Joint.RA3, -ang3, gain)
            self.set_target_angle(Joint.RA4, -ang4, gain)

    def set_initial_leg(self, leg) -> bool:

        ang1 = 0
        ang2 = 6.0
        ang3 = 18.0
        ang4 = -30.0
        ang5 = 18.0
        ang6 = -6.0

        gain = 7.0

        if (leg == BodyParts.LEG_LEFT):

            self.set_target_angle(Joint.LL1, ang1, gain)
            self.set_target_angle(Joint.LL2, ang2, gain)
            self.set_target_angle(Joint.LL3, ang3, gain)
            self.set_target_angle(Joint.LL4, ang4, gain)
            self.set_target_angle(Joint.LL5, ang5, gain)
            self.set_target_angle(Joint.LL6, ang6, gain)

        else:

            self.set_target_angle(Joint.RL1, ang1, gain)
            self.set_target_angle(Joint.RL2, -ang2, gain)
            self.set_target_angle(Joint.RL3, ang3, gain)
            self.set_target_angle(Joint.RL4, ang4, gain)
            self.set_target_angle(Joint.RL5, ang5, gain)
            self.set_target_angle(Joint.RL6, -ang6, gain)

    def set_current_angle(self, joint: Joint, angle):
        self.previous_joints_list[joint] = self.joints_list[
            joint].current_angle
        self.joints_list[joint].current_angle = angle

    def gettarget_angle(self, joint: Joint):
        return self.joints_list[joint].target_angle

    def update_speed(self, gain):
        for joint in Joint:
            self.set_angle_gain(joint, gain)

    def get_change_in_gyro_rate(self):
        return (self.gyro_rates[0] - self.prev_gyro_rates[0],
                self.gyro_rates[1] - self.prev_gyro_rates[1],
                self.gyro_rates[2] - self.prev_gyro_rates[2])

    def get_change_in_angle(self, joint: Joint):
        return self.joints_list[
            joint].current_angle - self.previous_joints_list[joint]

    def set_target_angle(self, joint: Joint, angle, gain=None):
        self.joints_list[joint].set_target_angle(angle)
        if gain is not None:
            self.set_angle_gain(joint, gain)

    def increase_target_angle(self,
                              joint: Joint,
                              angle_increase,
                              gain=None):
        self.joints_list[joint].set_target_angle(
            self.joints_list[joint].target_angle + angle_increase)

        if gain is not None:
            self.set_angle_gain(joint, gain)

    def get_scale(self, joint: Joint):
        return self.joints_list[joint].scale

    def set_angle_gain(self, joint: Joint, scale):
        self.joints_list[joint].scale = scale

    def initialise_joints(self):
        for joint in Joint:
            joint_range = joint.range
            self.joints_list[joint] = NaoJoint(joint_range[0],
                                               joint_range[1],
                                               2.0)

    def get_accel_rates(self):
        return self.accel_rates

    def set_accel_rates(self, accel_rates):
        self.accel_rates = accel_rates

    def set_gyro_rates(self, rates):
        self.prev_gyro_rates = self.gyro_rates
        self.gyro_rates = rates

    def get_gyro_rates(self):
        return self.gyro_rates

    def compute_torque(self, joint: Joint):

        nao_joint = self.joints_list[joint]
        gain = nao_joint.scale
        angle = nao_joint.target_angle

        current_angle = nao_joint.current_angle

        if angle >= nao_joint.max_angle:
            angle = nao_joint.max_angle

        elif angle <= nao_joint.min_angle:
            angle = nao_joint.min_angle

        if abs(angle - current_angle) < nao_joint.error_tolerance:
            return 0
        elif current_angle < angle:
            return math.radians(abs(angle - current_angle)) * gain
        elif current_angle > angle:
            return -math.radians(abs(angle - current_angle)) * gain
